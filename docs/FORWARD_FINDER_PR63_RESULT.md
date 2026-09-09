# Forward-Finder PR #63 Retrospective Calibration Result

Subject: `mirrornode/MIRRORNODE-CORE-HUB` PR #63
Historical exact head: `df645e26da389c4d035f4bc5f8d69d1de5824890`
Mode: retrospective seeded baseline

The original substring implementation recovered 8/8 seeded consequence classes
and reported precision 1.0, recall 1.0. Preserve that as the historical result,
not as evidence of predictive accuracy or current implementation behavior.
The input describes corrections and the matcher incorrectly treated that
vocabulary as support for defects.

The corrected implementation returns `UNKNOWN` with no predictions for that
same text. The expected-output fixture is generated from the public serializer.
Consequence families remain reusable review guidance; explicit observation
pairs test the narrowed interface separately.

The original self-trial timing assertion lacks verified immutable subject and
ordering evidence. It is UNVERIFIED and excluded from prospective metrics.
It cannot establish a prospective success or formally scored miss.
