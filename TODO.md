# Todos sorted by importance

1. Add a description for our program.
    * What does it do?
    * What is Q circle?
    * What data formats are supported?
2. [x] Add validation of separator + convertor to std backend input
3. Should we apply corrections for coupling losses? - yes, please add this option.
4. [x] Draw continuous Q circle on a Smith chart using coefficients a[0..2]
5. [x] Add axes labels to a Smith chart
6. Pretty-print results and errors (7 digits after dot). Try latex output.
7. Advanced output options (only frontend):
    * Option to choose output values precision
8. Add approximation for second chart (abs(S11) from f)
9. Add impedance input option (Z instread of S11)
    * additional field for omega
    * convertion to reflection coeffitient (thats how: <https://radioprog.ru/post/195>)
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

13. Do we need to calculate systematic errors? - yes, if its not too hard.
14. Add direct support for output files from different vna models
15. Make charts more interactive
16. Make an option to pass the whole program to .html site as a iframe
