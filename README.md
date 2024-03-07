# Test suite for SWB2

This repo holds a number of tests that are designed to demonstrate that the calculations made with SWB2 are consistent with the methods that are described as the basis for SWB2's internal calculations as documented in Westenbroek and others (2010, 2018). Each of the tests included here are an attempt to exercise particular functionality within the SWB2 code. A brief list of tests follows.

1. _Thornthwaite-Mather soil moisture retention_. This test demonstrates that the code included in SWB2 for determining the amount of soil moisture that may be extracted from a soil column is consistent with the use and application of the soil moisture retention tables included in the Thornthwaite-Mather (1957). 
2. _Runoff Curve Number_.
3. _Flow routing_.
4. _FAO-56 functionality_.
5. _NetCDF reading capability and fidelity_. This test demonstrates that the code is capable of reading and correctly georeferencing common gridded datasets distributed as netCDF files. There is much flexibility in the way in which a particular research group chooses to encode a dataset within one or more netCDF files. SWB2 has been coded to reliably read in the most common of these files. There will likely be edge cases that are not read in correctly.
