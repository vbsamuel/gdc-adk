# Definition of Coverage Complete

Coverage is complete only when all of the following are true:

1. Every changed public file has meaningful unit tests.
2. Every changed subsystem boundary has integration tests.
3. Every impacted end-to-end scenario has been mapped and exercised.
4. Negative paths relevant to changed behavior are asserted.
5. Typed outputs, side effects, and lineage effects are asserted.
6. Replay/resume behavior is asserted when relevant.
7. Static checks for naming, typing, and boundaries are clean or findings are explicitly accepted.
8. There are no empty tests, placeholder assertions, or smoke-only proxies for real behavior.
9. Traceability rows affected by the change have corresponding proving tests.
10. Reviewers can explain what is still untested and why.

Line coverage alone is insufficient.
