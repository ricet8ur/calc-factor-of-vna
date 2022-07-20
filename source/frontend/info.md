##### Usage:

App calculates the quality factor and its random error in the electric circuit
for the set of [vector analyzer](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) measuremets.

##### Input data

The measurements made by a vector network analyzer (set of frequencies and corresponding network parameters).
Main supported file format is .snp, but similar formats are accepted too. Noise data is not supported.

* Supported network parameters: S, Z
* Supported parameters representations:
real and imaginary; magnitude and angle; db and angle

##### Result

* Loaded and unloaded quality factor (q-factor) with random errors
* plot amplitude vs frequency
* [Smith chart](https://en.wikipedia.org/wiki/Smith_chart)

##### Calculation method

Calculation of Q-factor and random errors is based on the algorithm, described in [1-2].
Correction for coupling loss is implemented according to [3].

##### References

[1]: Random and Systematic Uncertainties of Reflection-Type Q-Factor Measurement with Network Analyzer (2003).
    DOI: 10.1109/TMTT.2002.807831

[2]: Data Processing For Q Factor Measurement (1994).
    DOI: 10.1109/ARFTG.1994.327064

[3]: Q Factor Measurements Using MATLAB (2011).
    ISBN: 978-1-60807-161-6

##### External links

[Github](https://github.com/ricet8ur/calc-factor-of-vna)

##### Alternatives

* http://scikit-rf.org/
* https://people.engineering.olemiss.edu/darko-kajfez/software/