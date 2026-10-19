# Development record

Protocol published at `43df0adeb08cbe7095fc991d140cd1c96ae32327`.
Initial complete sources published at `91e212aed9ac87a8f15a672a2fb15642cf50730e`.
Six development clouds completed under that source freeze. They are retained
in `development_initial/`, including the original source hashes and timings.

Before generating any targets, the relation builder was optimized: component
differences dt, dx, dy replace the strided three-component temporary. The test
remains dt>0 and dt*dt>dx*dx+dy*dy, with the same subtraction, multiplication and
two-term addition as before. No scientific rule, seed, numerical type, block
size, duration, candidate limit or decision threshold changed. A 2048-point
comparison produced exactly equal relation matrices (4,194,304 entries).
The independent scalar relation/count controls remain in the frozen suite.

The six development clouds are replayed under the final sources before targets.
Their complete discrete structures, relation/mark/colour hashes and invariant
numerical outputs must agree with the initial records. Both generations are
retained. Development outcomes cannot choose the primary arm or change a gate.
