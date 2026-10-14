// SPDX-License-Identifier: Apache-2.0
// RP2040 Pico adapter. Hardware build and electrical qualification are separate gates.
#include "core.hpp"
#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "hardware/watchdog.h"
#include <cstdio>
constexpr uint CS=17, SCK=18, MOSI=19, ENABLE=2;
static void output(uint32_t code, bool enabled, uint64_t, void*) {
    if (!enabled) gpio_put(ENABLE,0);
    // MCP4921: unbuffered reference, gain 1, active; LDAC tied to GND.
    const uint16_t word=uint16_t(0x3000u | code);
    const uint8_t bytes[2]={uint8_t(word>>8),uint8_t(word)};
    gpio_put(CS,0); spi_write_blocking(spi0,bytes,2); gpio_put(CS,1);
    if (enabled) gpio_put(ENABLE,1);
}
int main() {
    gpio_init(ENABLE); gpio_put(ENABLE,0); gpio_set_dir(ENABLE,GPIO_OUT);
    gpio_init(CS); gpio_put(CS,1); gpio_set_dir(CS,GPIO_OUT);
    spi_init(spi0,1000000);
    spi_set_format(spi0,8,SPI_CPOL_0,SPI_CPHA_0,SPI_MSB_FIRST);
    gpio_set_function(SCK,GPIO_FUNC_SPI); gpio_set_function(MOSI,GPIO_FUNC_SPI);
    acv::Core core(output,nullptr,true); acv::Receiver receiver;
    core.boot(time_us_64()/1000);
    stdio_init_all(); watchdog_enable(250,true);
    for (;;) {
        // time_us_64 preserves monotonic time beyond the 32-bit millisecond wrap.
        core.tick(time_us_64()/1000); watchdog_update();
        int c=getchar_timeout_us(0);
        if (c>=0) receiver.feed(uint8_t(c),[&](const uint8_t* packet) {
            uint8_t reply[acv::FRAME]; bool valid=core.handle(packet,reply,time_us_64()/1000);
            if (valid) { for (uint8_t b:reply) putchar_raw(b); stdio_flush(); }
            return valid;
        });
        tight_loop_contents();
    }
}
