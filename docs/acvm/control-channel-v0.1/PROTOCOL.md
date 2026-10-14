# ACV1 wire protocol

Version is fixed by ASCII magic `ACV1`. No other major version is accepted.
All numeric fields are unsigned little-endian integers. Frame length is 48 bytes.
This protocol is for an explicitly selected, locally attached reference device;
it provides corruption detection, not authentication or multi-client arbitration.

| Offset | Bytes | Request | Response |
| --- | --- | --- | --- |
| 0 | 4 | `ACV1` | `ACV1` |
| 4 | 1 | Opcode | Echoed opcode |
| 5 | 1 | 0 | 1 |
| 6 | 2 | Reserved, zero | Bit 0: hardware-declared adapter; bit 1: replay. Other bits zero |
| 8 | 4 | Nonzero session ID | Current device session ID |
| 12 | 4 | Command sequence | Echoed command sequence |
| 16 | 28 | Seven parameters; unused values zero | Error, state, commanded code, applied-point count, elapsed ms, boot-lifetime run counter, profile ID |
| 44 | 4 | CRC32 of all preceding 44 bytes | Same |

CRC32: reflected IEEE polynomial 0xEDB88320, initial/final XOR 0xFFFFFFFF;
equivalent to Python `zlib.crc32`. A session nonce comes from the OS random source.
It separates runs but is not a secret or a cryptographic challenge.
Profile ID: `0xAC010001`, name `pico-mcp4921-code-v1`.

| Opcode | Parameters in order | Allowed operation |
| --- | --- | --- |
| 1 OPEN | profile ID | Sequence 0, new nonzero session; outputs inactive, reset plan. Cannot replace a RUNNING session |
| 2 BEGIN | count, duration_ms, plan_crc32 | IDLE → LOADING; 1–64 points, 10–5000 ms |
| 3 POINT | index, at_ms, dac_code | LOADING; contiguous index, first time 0, spacing ≥10 ms, time ≤duration−10, code ≤3276 |
| 4 SEAL | none | All points present and full plan CRC correct: LOADING → READY |
| 5 START | none | READY → RUNNING; starts once on the device clock |
| 6 POLL | none | Read status and renew lease on a **new**, valid command; a replay does not renew |
| 7 STOP | none | Matching session; bypasses sequence gaps; requests zero and disables output |

Compiled plan: uint32 duration, uint32 point count, then count pairs of uint32
time and code. Plan CRC covers every byte including the header. SHA-256 in the
run record additionally binds the complete binary file.

States 0–6: IDLE, LOADING, READY, RUNNING, DONE, ABORTED, FAULT.
Errors 0–11: OK, FORMAT, SESSION, ORDER, RANGE, BAD_STATE, PLAN_CRC, LEASE,
LATE, CLOCK, REPLAY_CONFLICT, PROFILE_ERROR. Rejected commands do not advance
the accepted sequence. Valid POLL in FAULT consumes its sequence while returning
the latched error. STOP preserves an existing FAULT, DONE or ABORTED state.

The last accepted request is cached in full. An identical immediate retry gets
a fresh state response with the replay flag; it does not reapply any output or
renew the lease. A conflicting retry is rejected. Sequence wrap is rejected.
After another command has been accepted, an old request is out of order.
STOP bypasses this ordering restriction to remain usable after a lost ACK;
it never starts or resumes output.

Malformed full frames receive no response; they stop a RUNNING core. Leading
noise and partial frames cannot execute commands; receiver resynchronization
is bounded to one frame buffer. Noise can delay communication and thereby
cause lease expiry. Valid but rejected commands while RUNNING also latch FAULT.
This prioritizes stopping over availability on a dedicated control link.

Native model uses a monotonic host clock. Pico uses `time_us_64()/1000`.
The sequence is preloaded; USB timing does not schedule individual output edges.
The core checks the lease before advancing events. After 500 ms without a fresh
POLL, a missed event beyond 20 ms, or a backwards clock, it requests zero and
disables the enable output. A new session must be explicitly loaded to run again.
These checks cannot detect wrong electrical wiring, a stuck DAC, or clock drift
relative to an external time standard. See the independent measurement gate.

The hardware flag identifies the compiled adapter only. It is not attestation.
Firmware identity, actual board identity, electrical readback and optical state
must be recorded independently in a hardware test. No auto-discovery, auto-flash,
auto-reconnect, HTTP actuation API or browser actuator button is provided.
