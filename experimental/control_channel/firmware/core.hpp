// Copyright 2026 Thomas Gfeller. SPDX-License-Identifier: Apache-2.0
// Portable ACV1 state machine; no allocation, no device or host dependencies.
#pragma once
#include <cstdint>
#include <cstddef>
#include <cstring>

namespace acv {
constexpr uint32_t PROFILE = 0xAC010001;
constexpr size_t FRAME = 48;
constexpr uint32_t MAX_POINTS = 64, MAX_MS = 5000, MIN_MS = 10;
constexpr uint32_t LEASE_MS = 500, LATE_MS = 20, MAX_CODE = 3276;
enum Op : uint8_t { OPEN=1, BEGIN=2, POINT=3, SEAL=4, START=5, POLL=6, STOP=7 };
enum State : uint32_t { IDLE, LOADING, READY, RUNNING, DONE, ABORTED, FAULT };
enum Error : uint32_t { OK, FORMAT, SESSION, ORDER, RANGE, BAD_STATE, PLAN_CRC,
                       LEASE, LATE, CLOCK, REPLAY_CONFLICT, PROFILE_ERROR };
inline uint32_t get(const uint8_t* p) {
    return uint32_t(p[0]) | uint32_t(p[1])<<8 | uint32_t(p[2])<<16 | uint32_t(p[3])<<24;
}
inline void put(uint8_t* p, uint32_t v) {
    for (int i=0; i<4; ++i) p[i] = uint8_t(v >> (8*i));
}
inline uint32_t crc(const uint8_t* p, size_t n) {
    uint32_t c=0xffffffff;
    while (n--) { c ^= *p++; for (int i=0;i<8;++i) c = (c>>1) ^ (0xedb88320u & (0u-(c&1))); }
    return ~c;
}
struct Point { uint32_t ms, code; };
using Output = void (*)(uint32_t code, bool enabled, uint64_t now, void* context);

class Core {
    Output output_; void* context_; bool hardware_;
    Point points_[MAX_POINTS]{};
    uint32_t count_=0, loaded_=0, duration_=0, plan_crc_=0, last_seq_=0;
    uint8_t previous_[FRAME]{}; bool have_previous_=false;
    uint64_t start_=0, lease_=0, clock_=0;
    bool have_clock_=false;
    void emit(uint32_t value, bool enabled, uint64_t now) {
        code=value; output_(value, enabled, now, context_);
    }
    void fail(Error why, uint64_t now) { state=FAULT; fault=why; emit(0,false,now); }
    bool zeros(const uint8_t* r, unsigned from) const {
        for (unsigned i=from; i<7; ++i) if (get(r+16+4*i)) return false;
        return true;
    }
    void reply(const uint8_t* r, uint8_t* out, Error e, bool replay) const {
        std::memset(out,0,FRAME); std::memcpy(out,"ACV1",4);
        out[4]=r[4]; out[5]=1; out[6]=(hardware_?1:0) | (replay?2:0);
        put(out+8,session); put(out+12,get(r+12)); put(out+16,e);
        put(out+20,state); put(out+24,code); put(out+28,applied);
        put(out+32,elapsed); put(out+36,runs); put(out+40,PROFILE);
        put(out+44,crc(out,44));
    }
public:
    uint32_t session=0, code=0, applied=0, elapsed=0, runs=0;
    State state=IDLE; Error fault=OK;
    Core(Output out, void* context, bool hardware=false): output_(out),context_(context),hardware_(hardware) {}
    void boot(uint64_t now) { emit(0,false,now); clock_=now; have_clock_=true; }
    void tick(uint64_t now) {
        if (have_clock_ && now<clock_) { fail(CLOCK,now); return; }
        clock_=now; have_clock_=true;
        if (state!=RUNNING) return;
        const uint64_t delta=now-start_;
        elapsed=uint32_t(delta>MAX_MS?MAX_MS:delta);
        if (now-lease_>=LEASE_MS) { fail(LEASE,now); return; }
        // Never skip overdue events and subsequently claim a completed sequence.
        const uint32_t due=applied<count_ ? points_[applied].ms : duration_;
        if (delta>uint64_t(due)+LATE_MS) { fail(LATE,now); return; }
        if (applied<count_ && delta>=due) {
            emit(points_[applied].code,true,now); ++applied;
        }
        if (delta>=duration_) {
            if (applied!=count_) { fail(LATE,now); return; }
            state=DONE; elapsed=duration_; emit(0,false,now);
        }
    }
    // false: malformed transport frame; no response. Output is stopped if running.
    bool handle(const uint8_t* r, uint8_t* out, uint64_t now) {
        tick(now);
        if (std::memcmp(r,"ACV1",4) || r[5] || r[6] || r[7] || get(r+44)!=crc(r,44)) {
            if (state==RUNNING) fail(FORMAT,now);
            return false;
        }
        uint32_t sid=get(r+8), seq=get(r+12), a=get(r+16), b=get(r+20), c=get(r+24);
        Error e=OK; bool replay=false;
        if (r[4]==OPEN) {
            if (!sid || seq || a!=PROFILE || !zeros(r,1)) e=PROFILE_ERROR;
            else if (sid==session) {
                if (have_previous_ && !std::memcmp(previous_,r,FRAME)) replay=true;
                else e=REPLAY_CONFLICT;
            } else if (state==RUNNING) e=BAD_STATE;
            else {
                session=sid; last_seq_=0; loaded_=0; count_=0; applied=0; elapsed=0;
                state=IDLE; fault=OK; emit(0,false,now);
                std::memcpy(previous_,r,FRAME); have_previous_=true;
            }
        } else if (!sid || sid!=session) e=SESSION;
        else if (r[4]==STOP && zeros(r,0)) {
            // Session-bound stop bypasses sequence gaps after a lost ACK.
            // Terminal states remain terminal, including the original fault reason.
            if (state!=FAULT && state!=DONE && state!=ABORTED) state=ABORTED;
            emit(0,false,now); e=fault;
            // Prevent replaying a cached START as a new run; START requires READY.
        } else if (have_previous_ && seq==last_seq_) {
            if (std::memcmp(previous_,r,FRAME)) e=REPLAY_CONFLICT;
            else { replay=true; e=fault; }
        } else if (!seq || last_seq_==0xffffffffu || seq!=last_seq_+1) e=ORDER;
        else {
            switch (r[4]) {
            case BEGIN:
                if (state!=IDLE) e=BAD_STATE;
                else if (!a || a>MAX_POINTS || b<MIN_MS || b>MAX_MS || !zeros(r,3)) e=RANGE;
                else { count_=a; duration_=b; plan_crc_=c; loaded_=0; state=LOADING; }
                break;
            case POINT:
                if (state!=LOADING) e=BAD_STATE;
                else if (a!=loaded_ || a>=count_ || c>MAX_CODE || b>=duration_ ||
                         (a==0 ? b!=0 : b<points_[a-1].ms+MIN_MS) ||
                         duration_-b<MIN_MS || !zeros(r,3)) e=RANGE;
                else { points_[loaded_++]={b,c}; }
                break;
            case SEAL: {
                if (state!=LOADING || loaded_!=count_) { e=BAD_STATE; break; }
                if (!zeros(r,0)) { e=FORMAT; break; }
                uint8_t plan[8+MAX_POINTS*8]; put(plan,duration_); put(plan+4,count_);
                for (uint32_t i=0;i<count_;++i) { put(plan+8+i*8,points_[i].ms); put(plan+12+i*8,points_[i].code); }
                if (crc(plan,8+count_*8)!=plan_crc_) e=PLAN_CRC;
                else state=READY;
                break;
            }
            case START:
                if (state!=READY || runs==0xffffffffu) e=BAD_STATE;
                else if (!zeros(r,0)) e=FORMAT;
                else { state=RUNNING; start_=now; lease_=now; applied=0; elapsed=0; ++runs; tick(now); }
                break;
            case POLL:
                if (!zeros(r,0)) e=FORMAT;
                else { lease_=now; e=fault; }
                break;
            default: e=FORMAT;
            }
            // Valid fault-status polls also consume their sequence number.
            if (e==OK || (r[4]==POLL && e==fault && zeros(r,0))) {
                last_seq_=seq; std::memcpy(previous_,r,FRAME); have_previous_=true;
            }
        }
        if (e!=OK && state==RUNNING) fail(e,now);
        reply(r,out,e,replay); return true;
    }
};

// Bounded stream resynchronization; corrupt frames never execute commands.
class Receiver {
    uint8_t data_[FRAME]{}; size_t used_=0;
public:
    template<class Handler> void feed(uint8_t byte, Handler handle) {
        data_[used_++]=byte;
        while (used_ && std::memcmp(data_,"ACV1",used_<4?used_:4)) {
            --used_; std::memmove(data_,data_+1,used_);
        }
        if (used_==FRAME) {
            bool good=handle(data_);
            if (good) used_=0;
            else { --used_; std::memmove(data_,data_+1,used_); }
        }
    }
};
} // namespace acv
