// SPDX-License-Identifier: Apache-2.0
// Native execution of the production protocol/sequencer core, with a LOGGED MODEL output.
#include "core.hpp"
#include <chrono>
#include <cstdio>
#include <poll.h>
#include <unistd.h>
#include <cerrno>
static uint64_t clock_ms() {
    return std::chrono::duration_cast<std::chrono::milliseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static void output(uint32_t code, bool enabled, uint64_t now, void*) {
    std::fprintf(stderr,"{\"model_ms\":%llu,\"code\":%u,\"enabled\":%s}\n",
        static_cast<unsigned long long>(now),code,enabled?"true":"false");
    std::fflush(stderr);
}
int main() {
    acv::Core core(output,nullptr); acv::Receiver receiver; core.boot(clock_ms());
    bool connected=true;
    for (;;) {
        core.tick(clock_ms());
        // A disconnected host must leave the device clock/lease running.
        if (!connected && core.state!=acv::RUNNING) break;
        pollfd fd{connected?STDIN_FILENO:-1,POLLIN,0}; int ready=poll(&fd,1,1);
        if (ready<0 && errno!=EINTR) return 2;
        if (ready>0 && (fd.revents&POLLIN)) {
            uint8_t byte; if (read(STDIN_FILENO,&byte,1)!=1) {connected=false;continue;}
            receiver.feed(byte,[&](const uint8_t* packet) {
                uint8_t reply[acv::FRAME]; bool valid=core.handle(packet,reply,clock_ms());
                if (valid && write(STDOUT_FILENO,reply,sizeof(reply))!=sizeof(reply)) _exit(3);
                return valid;
            });
        }
        if (ready>0 && (fd.revents&(POLLHUP|POLLERR|POLLNVAL))) connected=false;
    }
    return 0;
}
