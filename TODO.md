# Todos sorted by importance

1. Do we need to calculate systematic errors?
2. Should we apply corrections for coupling losses?
3. Add validation of separator + convertor to std backend input
4. Add impedance data format:
    * additional field for omega
    * convertion to reflection coeffitient (how?)

5. Draw continuous Q circle on a Smith chart using coefficients a[0..2]
6. Add axes labels to a Smith chart
7. Pretty-print results and errors (7 digits after dot)
8. Plot another chart: abs(S11) from f
9. Make all computations extra precise:
    * import sympy.mpmath as mp ..?
    * from sympy.mpmath import *  ..?
    * mp.dps = ~50
    * make sure that result' ~ result
    * increase mp.dps while 7 digits after dot are not stable
10. Advanced file loading:
    * Show file preview
    * Options to skip first and last lines
11. Add direct support for output files from different vna models
12. Make charts more interactive
