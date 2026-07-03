# Test suite for SWB2

This repo holds a number of tests that are designed to demonstrate that the calculations made with SWB2 are consistent with the methods that are described as the basis for SWB2's internal calculations as documented in Westenbroek and others (2010, 2018). Each of the tests included here are an attempt to exercise particular functionality within the SWB2 code. A brief list of tests follows.

1. _Thornthwaite-Mather soil moisture retention_. This test demonstrates that the code included in SWB2 for determining the amount of soil moisture that may be extracted from a soil column is consistent with the use and application of the soil moisture retention tables included in the Thornthwaite-Mather (1957). 
2. _Runoff Curve Number_. This test demonstrates that SWB2's implementation of the SCS Curve Number runoff calculation — including the modified initial abstraction (Ia = 0.05S), antecedent runoff condition adjustment, and frozen ground enhancement — produces results consistent with an independent Python reimplementation of the same algorithms.
3. _Flow routing_. This test uses a synthetic 6×6 grid domain with a known D8 flow direction pattern to verify that SWB2 correctly routes runoff from upstream cells to downstream cells and conserves mass at the outlet.
4. _FAO-56 crop coefficient curves_. This test demonstrates that SWB2's date-based FAO-56 crop coefficient (Kcb) curve construction is consistent with a Python reimplementation. A secondary comparison against the independently-developed pyfao56 package (Thorp, 2022) exercises the full dual-Kc water balance.
5. _NetCDF reading capability and fidelity_. This test demonstrates that the code is capable of reading and correctly georeferencing common gridded datasets distributed as netCDF files. There is much flexibility in the way in which a particular research group chooses to encode a dataset within one or more netCDF files. SWB2 has been coded to reliably read in the most common of these files. There will likely be edge cases that are not read in correctly.


## Python environment setup

The Jupyter notebooks in this repository require a Python environment with several scientific packages. To create the environment using [mamba](https://mamba.readthedocs.io/):

```bash
mamba env create -f environment.yml
mamba activate swb2_tests
```

Then launch JupyterLab from the `jupyter/` directory:

```bash
cd jupyter
jupyter lab
```

## Running the tests

Each notebook is self-contained. It runs SWB2 (from `bin/swb2.exe`), executes a Python reimplementation of the same calculations, and compares the results. Notebooks create output in `test__<name>/output/` and `test__<name>/logfiles/` directories which are regenerated on each run.

THE CURRENT VERSION OF SWB2 INCLUDED IN 'bin' IS v2.4.0-rc0.

Notebooks should be run in order (01 through 05) since earlier notebooks verify foundational functionality.


Disclaimer
----------
This software is in the public domain because it contains materials that originally came from the U.S. Geological Survey, an agency of the United States Department of Interior. For more information, see the official USGS copyright policy at [http://www.usgs.gov/visual-id/credit_usgs.html#copyright](http://www.usgs.gov/visual-id/credit_usgs.html#copyright)

This information is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The information has not received final approval by the U.S. Geological Survey (USGS) and is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the information. Although this software program has been used by the USGS, no warranty, expressed or implied, is made by the USGS or the U.S. Government as to the accuracy and functioning of the program and related program material nor shall the fact of distribution constitute any such warranty, and no responsibility is assumed by the USGS in connection therewith.

This software is provided "AS IS."


References
----------

Thorp, K.R., 2022, pyfao56: FAO-56 evapotranspiration in Python: SoftwareX 19, 101208.

Westenbroek, S.M., Kelson, V.A., Dripps, W.R., Hunt, R.J., and Bradbury, K.R., 2010, SWB: A modified Thornthwaite-Mather Soil-Water-Balance code for estimating groundwater recharge: Techniques and Methods 6-A31, accessed March 7, 2024, at https://pubs.usgs.gov/publication/tm6A31.

Westenbroek, S.M., Engott, J.A., Kelson, V.A., and Hunt, R.J., 2018, A Soil-Water-Balance code  for estimating net infiltration and other water-budget components: U. S. Geological Survey Techniques and Methods book 6, chap. A59, 118 p., accessed March 7, 2024, at https://doi.org/10.3133/tm6A59.
