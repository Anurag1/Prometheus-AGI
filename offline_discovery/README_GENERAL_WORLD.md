# General-world offline discovery

This benchmark removes the polynomial-regression assumption used by the earlier experiment.

The hidden simulator is inaccessible to the discovery procedure. The agent receives only paired local observations `(x,t,y)` and searches a generic sparse composition of primitive relationships.

Recovered theory:

`y = 5 + x*t + (2*t - 3*x)`

Held-out verification:

| x | t | predicted | observed |
|---:|---:|---:|---:|
| 7 | 3 | 11 | 11 |
| -4 | 5 | 7 | 7 |
| 6 | -3 | -37 | -37 |
| 9 | 2 | 0 | 0 |

Maximum error: `0`.

Network access is blocked by the inherited benchmark isolation layer.

This is evidence of representation discovery within a declared primitive language, not open-ended scientific discovery. The next escalation is to let the system invent new primitives from raw state transitions rather than supplying the primitive library.
