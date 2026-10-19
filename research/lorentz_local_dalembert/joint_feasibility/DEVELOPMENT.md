# Development history before fresh targets

The initial protocol was public at
`8647afdc5177600251faf2cc08e3674568d6b5ee`. All development variants use the
same six declared seeds; none are confirmation data.

1. `development-v1`: stopped before the first completed cloud because the
   physical-event mask removed the artificial top probe from the old longest
   chain's successor set. The old inner baseline must use the unchanged Poset
   class (neither boundary probe can be an interior event there). This was
   repaired; the augmented event counts continue to use PhysicalPoset.
2. `development-v2`: initial fixed temporal supports, 64 landmarks per side,
   same-side triples only. Six clouds complete; no jointly selected support.
   Both low-density clouds fail temporal counts. Dense clouds produce only
   three and zero count-qualified triples.
3. `development-v3`: temporal points also adapted to count scale, frame pool
   increased to 256 per side. All six complete. Dense clouds supply 2,888 and
   3,925 count-qualified triples over the three scales; none meet the original
   signature/condition gate. No guard threshold changed.
4. `development-v4`: allow one frame with mixed past/future landmarks, 128
   candidates per side. Batched Gram computations are cross-checked against
   scalar formulas. Both dense clouds pass selection and hidden recolouring.
   One middle-density cloud is selected but fails hidden half-count/Gram gates.
   These observations motivate the frozen candidate; they are not validation.
5. `development-final`: identical inference to v4; stronger software controls
   add an exhaustive small-chain mixed-triple oracle and marked relabelling /
   time reversal on the middle-density example (which has a selected witness).

Each older execution preserves its manifest and matching new-module source
files in its `sources` directory. Unmodified inherited sources are available
at the initial public protocol commit. The earlier failed runner is also
retained. Intermediate code was locally developed; public protocol revision
and the complete final code are frozen together before the target run.

Mixed landmarks do not add another frame or change the Gram identity. For
timelike comparable pairs, q(a,b)=-g(a-b,a-b), so
g(a-x,b-x)=(-q(a,x)-q(b,x)+q(a,b))/2 holds for either time orientation.
Every chosen landmark remains comparable to the root and every support.

The second colouring is never used to retry a frame, move a support or pick
a different scale. It is a conditional stability audit on the same physical
cloud, not independent physical data or a 95% guarantee.
