// SPDX-License-Identifier: Apache-2.0
// Virtual-clock fault injection. Expectations are explicit, not a second Core run.
#include "core.hpp"
#include <array>
#include <vector>
#include <stdexcept>
#include <cstdio>
#include <string>
using Frame=std::array<uint8_t,48>;
struct Event { uint32_t code; bool enabled; uint64_t ms; };
static void require(bool b,const char* why) { if (!b) throw std::runtime_error(why); }
static Frame request(uint8_t op,uint32_t sid,uint32_t seq,uint32_t a=0,uint32_t b=0,uint32_t c=0) {
    Frame r{}; std::memcpy(r.data(),"ACV1",4); r[4]=op;
    acv::put(r.data()+8,sid); acv::put(r.data()+12,seq); acv::put(r.data()+16,a);
    acv::put(r.data()+20,b); acv::put(r.data()+24,c); acv::put(r.data()+44,acv::crc(r.data(),44)); return r;
}
struct Fixture {
    std::vector<Event> events;
    acv::Core core;
    uint32_t sid=17,seq=0; uint64_t now=0;
    static void record(uint32_t code,bool enable,uint64_t now,void* ctx) { static_cast<Fixture*>(ctx)->events.push_back({code,enable,now}); }
    Fixture():core(record,this) { core.boot(0); }
    Frame send(Frame r) { Frame out{}; require(core.handle(r.data(),out.data(),now),"no reply"); return out; }
    Frame cmd(uint8_t op,uint32_t a=0,uint32_t b=0,uint32_t c=0) { auto out=send(request(op,sid,seq++,a,b,c)); require(acv::get(out.data()+16)==0,"unexpected rejection"); return out; }
    void open() { cmd(acv::OPEN,acv::PROFILE); }
    void load(uint32_t duration=1000,uint32_t code=1000) {
        open(); uint8_t plan[16]; acv::put(plan,duration); acv::put(plan+4,1); acv::put(plan+8,0); acv::put(plan+12,code);
        cmd(acv::BEGIN,1,duration,acv::crc(plan,16)); cmd(acv::POINT,0,0,code); cmd(acv::SEAL);
    }
    void inactive(acv::State s) { require(core.state==s && core.code==0 && !events.back().enabled,"output not inactive"); }
};
int main() {
    std::vector<std::string> names;
    auto test=[&](const char* name,auto fn) { fn(); names.emplace_back(name); };
    try {
        test("boot_and_open_output_zero",[] { Fixture f; f.inactive(acv::IDLE); f.open(); f.inactive(acv::IDLE); });
        test("nominal_sequence_exact_output",[] { Fixture f; f.load(); f.cmd(acv::START); require(f.core.code==1000 && f.core.runs==1,"start"); for (int t=100;t<1000;t+=100) {f.now=t;f.cmd(acv::POLL);} f.core.tick(1000);f.inactive(acv::DONE); require(f.events.size()==4,"wrong event count"); });
        test("duplicate_start_is_idempotent",[] { Fixture f;f.load();auto r=request(acv::START,f.sid,f.seq); f.send(r); f.now=10;auto out=f.send(r);require(out[6]&2,"missing replay bit");require(f.core.runs==1 && f.events.size()==3,"duplicate output"); });
        test("completed_sequence_cannot_restart",[] { Fixture f;f.load(10);auto r=request(acv::START,f.sid,f.seq++);f.send(r);f.core.tick(10);f.now=10;f.send(r);f.inactive(acv::DONE);auto out=f.send(request(acv::START,f.sid,f.seq));require(acv::get(out.data()+16)==acv::BAD_STATE && f.core.runs==1,"restart accepted"); });
        test("lease_expires_at_500ms",[] { Fixture f;f.load();f.cmd(acv::START);f.core.tick(499);require(f.core.state==acv::RUNNING,"early timeout");f.core.tick(500);f.inactive(acv::FAULT);require(f.core.fault==acv::LEASE,"wrong fault"); });
        test("poll_renews_lease",[] { Fixture f;f.load();f.cmd(acv::START);f.now=400;f.cmd(acv::POLL);f.core.tick(899);require(f.core.state==acv::RUNNING,"renewal ignored");f.core.tick(900);f.inactive(acv::FAULT); });
        test("replayed_poll_does_not_renew",[] { Fixture f;f.load();f.cmd(acv::START);f.now=100;auto r=request(acv::POLL,f.sid,f.seq);f.send(r);f.now=400;f.send(r);f.core.tick(600);f.inactive(acv::FAULT); });
        test("stop_survives_sequence_gap",[] { Fixture f;f.load();f.cmd(acv::START);f.send(request(acv::STOP,f.sid,999));f.inactive(acv::ABORTED);auto out=f.send(request(acv::START,f.sid,f.seq));require(acv::get(out.data()+16)==acv::BAD_STATE,"restart after stop"); });
        test("wrong_session_stops_running_output",[] { Fixture f;f.load();f.cmd(acv::START);f.send(request(acv::POLL,123,f.seq));f.inactive(acv::FAULT); });
        test("out_of_order_stops_running_output",[] { Fixture f;f.load();f.cmd(acv::START);auto out=f.send(request(acv::POLL,f.sid,99));require(acv::get(out.data()+16)==acv::ORDER,"out of order");f.inactive(acv::FAULT); });
        test("same_sequence_changed_payload_rejected",[] { Fixture f;f.load();f.cmd(acv::START);auto out=f.send(request(acv::POLL,f.sid,f.seq-1));require(acv::get(out.data()+16)==acv::REPLAY_CONFLICT,"conflicting replay");f.inactive(acv::FAULT); });
        test("plan_crc_rejected_before_ready",[] { Fixture f;f.open();f.cmd(acv::BEGIN,1,1000,0);f.cmd(acv::POINT,0,0,100);auto out=f.send(request(acv::SEAL,f.sid,f.seq));require(acv::get(out.data()+16)==acv::PLAN_CRC && f.core.state==acv::LOADING,"bad plan ready"); });
        test("partial_load_cannot_start",[] { Fixture f;f.open();f.cmd(acv::BEGIN,2,1000,0);auto out=f.send(request(acv::START,f.sid,f.seq));require(acv::get(out.data()+16)==acv::BAD_STATE && f.core.code==0,"partial start"); });
        test("buffer_capacity_and_duration_bounds",[] { for (auto n:{0u,65u,0xffffffffu}) { Fixture f;f.open();auto out=f.send(request(acv::BEGIN,f.sid,f.seq,n,1000,0));require(acv::get(out.data()+16)==acv::RANGE,"capacity"); } for(auto d:{0u,9u,5001u,0xffffffffu}) {Fixture f;f.open();auto out=f.send(request(acv::BEGIN,f.sid,f.seq,1,d,0));require(acv::get(out.data()+16)==acv::RANGE,"duration");} });
        test("dac_code_bounds",[] { Fixture f;f.open();f.cmd(acv::BEGIN,1,1000,0);auto out=f.send(request(acv::POINT,f.sid,f.seq,0,0,3277));require(acv::get(out.data()+16)==acv::RANGE && f.core.code==0,"DAC bound"); });
        test("point_time_and_order_bounds",[] { Fixture f;f.open();f.cmd(acv::BEGIN,2,1000,0);auto out=f.send(request(acv::POINT,f.sid,f.seq,0,1,1));require(acv::get(out.data()+16)==acv::RANGE,"nonzero first tick");f.cmd(acv::POINT,0,0,1);out=f.send(request(acv::POINT,f.sid,f.seq,1,9,1));require(acv::get(out.data()+16)==acv::RANGE,"spacing"); });
        test("timing_overrun_latches_fault",[] { Fixture f;f.load(100);f.cmd(acv::START);f.core.tick(121);f.inactive(acv::FAULT);require(f.core.fault==acv::LATE,"late event not detected"); });
        test("clock_reversal_latches_fault",[] { Fixture f;f.load();f.cmd(acv::START);f.core.tick(10);f.core.tick(9);f.inactive(acv::FAULT);require(f.core.fault==acv::CLOCK,"clock fault"); });
        test("64bit_clock_crosses_32bit_boundary",[] { Fixture f;f.now=uint64_t(0xffffffffu)-20;f.load(100);f.cmd(acv::START);f.core.tick(f.now+100);f.inactive(acv::DONE); });
        test("corrupt_crc_stops_running_output",[] { Fixture f;f.load();f.cmd(acv::START);auto r=request(acv::POLL,f.sid,f.seq);r[30]^=1;Frame out{};require(!f.core.handle(r.data(),out.data(),f.now),"bad CRC accepted");f.inactive(acv::FAULT); });
        test("every_single_bit_corruption_rejected",[] { for(size_t bit=0;bit<384;++bit) { Fixture f;auto r=request(acv::OPEN,17,0,acv::PROFILE);r[bit/8]^=uint8_t(1u<<(bit%8));Frame out{};require(!f.core.handle(r.data(),out.data(),0),"single bit accepted");require(f.core.session==0,"corruption changed state");} });
        test("reserved_request_fields_rejected",[] { Fixture f;auto r=request(acv::OPEN,17,0,acv::PROFILE);r[7]=1;acv::put(r.data()+44,acv::crc(r.data(),44));Frame out{};require(!f.core.handle(r.data(),out.data(),0),"reserved header accepted"); });
        test("stream_resynchronizes_after_noise",[] { Fixture f;acv::Receiver receiver;int replies=0;auto feed=[&](uint8_t b){receiver.feed(b,[&](const uint8_t* p){Frame out{};bool valid=f.core.handle(p,out.data(),0);replies+=valid;return valid;});};for(int i=0;i<100;++i)feed(0xff);auto bad=request(acv::OPEN,17,0,acv::PROFILE);bad[30]^=1;for(auto b:bad)feed(b);auto good=request(acv::OPEN,17,0,acv::PROFILE);for(auto b:good)feed(b);require(replies==1 && f.core.session==17,"resync failed"); });
        test("new_session_required_after_fault",[] { Fixture f;f.load();f.cmd(acv::START);f.now=500;f.core.tick(f.now);f.send(request(acv::STOP,f.sid,99));require(f.core.fault==acv::LEASE,"fault erased");auto out=f.send(request(acv::OPEN,18,0,acv::PROFILE));require(acv::get(out.data()+16)==0 && f.core.state==acv::IDLE,"reset session failed"); });
        test("unknown_profile_rejected",[] {Fixture f;auto out=f.send(request(acv::OPEN,17,0,0));require(acv::get(out.data()+16)==acv::PROFILE_ERROR && f.core.session==0,"profile accepted");});
        test("full_buffer_executes_64_points",[] { Fixture f;f.open();uint8_t plan[520];acv::put(plan,640);acv::put(plan+4,64);for(uint32_t i=0;i<64;++i){acv::put(plan+8+i*8,i*10);acv::put(plan+12+i*8,i);}f.cmd(acv::BEGIN,64,640,acv::crc(plan,520));for(uint32_t i=0;i<64;++i)f.cmd(acv::POINT,i,i*10,i);f.cmd(acv::SEAL);f.cmd(acv::START);for(int i=1;i<64;++i){f.now=i*10;f.cmd(acv::POLL);require(f.core.code==uint32_t(i),"wrong code");}f.core.tick(640);f.inactive(acv::DONE);require(f.core.applied==64,"missing point");});
        test("plan_corruption_after_byte_256_rejected",[] {Fixture f;f.open();uint8_t plan[520];acv::put(plan,1000);acv::put(plan+4,64);for(uint32_t i=0;i<64;++i){acv::put(plan+8+i*8,i*10);acv::put(plan+12+i*8,i);}f.cmd(acv::BEGIN,64,1000,acv::crc(plan,520));for(uint32_t i=0;i<64;++i)f.cmd(acv::POINT,i,i*10,i==50?999:i);auto out=f.send(request(acv::SEAL,f.sid,f.seq));require(acv::get(out.data()+16)==acv::PLAN_CRC,"late corruption accepted");});
        std::printf("{\"status\":\"PASS\",\"cases\":[");
        for(size_t i=0;i<names.size();++i)std::printf("%s\"%s\"",i?",":"",names[i].c_str());
        std::printf("]}\n"); return 0;
    } catch(const std::exception& e) { std::fprintf(stderr,"After %zu passes: %s\n",names.size(),e.what()); return 1; }
}
