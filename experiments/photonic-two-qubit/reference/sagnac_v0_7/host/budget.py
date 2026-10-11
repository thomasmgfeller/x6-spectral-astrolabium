#!/usr/bin/env python3
"""Design arithmetic, not measured FPGA timing or an arrival-process guarantee."""
import json
import math
from pathlib import Path

def calculate():
    hz=50_000_000;cycles=5
    rates=[100_000]*4;watermarks=1000
    envelope_rate=4_000_000;pause_s=100e-6;burst_events=512
    bound=math.ceil(burst_events+envelope_rate*pause_s)
    return {
      "status":"ASSUMED_DESIGN_BUDGET_NOT_HARDWARE_QUALIFIED",
      "assumed_core_clock_hz":hz,"max_logic_cycles_per_item":cycles,
      "conditional_service_events_per_second":hz/cycles,
      "assumed_counts_per_second_per_channel":rates,"watermarks_per_second":watermarks,
      "conditional_nominal_load_fraction":(sum(rates)+watermarks)/(hz/cycles),
      "fifo_arrival_envelope":{"burst_events":burst_events,"sustained_event_rate":envelope_rate,
         "max_service_pause_seconds":pause_s,"bound_b_plus_rT":bound,
         "selected_depth_for_this_example":1<<(bound-1).bit_length()},
      "uart":{"frame_bytes":244,"clocks_per_bit":50,"bits_per_byte_8N1":10,
         "baud_at_assumed_clock":hz/50,"upper_scheduling_clocks_per_byte":501,
         "approx_frame_time_seconds_with_interbyte_clock":244*501/hz},
      "unverified":["Quartus timing of division, multiplication, CRC and output mux",
         "TDC, channel merge and CDC latency and throughput","detector pulse acquisition",
         "actual burst envelope and service interruption bound","physical UART bit error rate"]}

if __name__=="__main__":
    out=Path(__file__).resolve().parents[1]/"examples/design_budget.json"
    out.write_text(json.dumps(calculate(),indent=2)+"\n")
    print(out)
