# Todos sorted by importance

1. Add a description for our program.
    * What does it do?
    * What is Q circle?
    * What data formats are supported?
2. [x] Change startup file to main.py and remove os and sys calls from frontend. Pass calc function to frontend function as an argument.
3. [x] Add validation of separator + convertor to std backend input
4. Should we apply corrections for coupling losses? - yes, please add this option.
5. Draw continuous Q circle on a Smith chart using coefficients a[0..2]
6. Add axes labels to a Smith chart
7. Pretty-print results and errors (7 digits after dot). Try latex output.
8. Plot second chart: abs(S11) from f
9. Add impedance data format (only frontend):
    * additional field for omega
    * convertion to reflection coeffitient (how?)
10. Codestyle fix:
    * Format all code files
    * Make a good code structure... If you can.
11. Make all computations extra precise:
    * import sympy.mpmath as mp ..?
    * from sympy.mpmath import *  ..?
    * mp.dps = ~50 or something else.
    * make sure that result' ~ result
    * increase mp.dps while 7 digits after dot are not stable

12. Advanced file loading:
    * Show file preview
    * Options to skip first and last lines
13. Advanced output options (only frontend):
    * Option to choose output values precision
14. Do we need to calculate systematic errors? - yes, if its not too hard.
15. Add direct support for output files from different vna models
16. Make charts more interactive
17. Make an option to pass the whole program to .html site as a iframe
