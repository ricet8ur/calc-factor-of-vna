# Todos sorted by importance

1. [x] Add a description for frontend.
    * What is calculated? The format of the result
    * What is Q circle?
    * What data formats are supported?
2. [x] Demo
3. [x]Support .snp
    * .s3p and more
4. [x] Add button to copy choosen fragment to compare with other programs.
5. [x] Advanced output options (only frontend):
    * Option to choose output values precision
6. [x] Add approximation for second chart (abs(S) from f)
7. [x] Add impedance input option (Z)
    * additional field for omega | from .snp
    * convertion to reflection coeffitient (explanation: <https://radioprog.ru/post/195>)
8. Codestyle fix:
    * Format all code files
    * Make a good code structure... If you can.
9. Make all computations extra precise:
    * import sympy.mpmath as mp ..?
    * from sympy.mpmath import *  ..?
    * mp.dps = ~50 or something else.
    * make sure that result' ~ result
    * increase mp.dps while 7 digits after dot are not stable
    * Don't do it, it is already taking ~3 seconds for 30000 input lines
10. [x] Advanced file loading:
    * Show file preview
    * Options to skip first and last lines
11. [x] Advanced file preview: highlight choosen data fragments
12. [x] Make charts more interactive
<!-- Add direct support for output files from different vna models? Supported formats: .snp, .csv or similar -->
