# Todos sorted by importance

1. Add a description for frontend.
    * What is calculated? The format of the result
    * What is Q circle?
    * What data formats are supported?
2. Demo
3. [x] Support .snp
4. Add window with copyable fragment of choosen data to compare with other programs.
5. Advanced output options (only frontend):
    * Option to choose output values precision
6. Add approximation for second chart (abs(S11) from f)
7. Add impedance input option (Z)
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
10. [x] Advanced file loading:
    * Show file preview
    * Options to skip first and last lines
11. Advanced file preview: .snp support for .s2p (or more) 
12. [x] Make charts more interactive
13. Make an option to pass the whole program to .html site via iframe? - It works, but where to host?
14. Add support lines for smith chart?
<!-- Add direct support for output files from different vna models? Supported formats: .snp, .csv or similar -->
<!-- Do we need to calculate systematic errors? - yes, if its not too hard. After some considerations... Rather not -->
