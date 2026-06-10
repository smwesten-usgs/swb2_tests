# Test of netCDF file read functionality: summary

This notebook summarizes the results of netCDF file read capability for SWB2. More importantly, this includes the ability of SWB to translate the SWB project grid coordinates into the native coordinates used by each of the weather data grids. _The purpose of these tests is to verify that commonly used files that contain daily weather data can be read into SWB without distortion, warping, or inversion (north-to-south or east-to-west)_. A summary table is first, followed by a discussion of each of the individual data sources tested, along with notes on what SWB2 control file items needed to be included.

Note that this testing is not automated in any way. The tests here represent results for a particular dataset as run with a specific SWB2 version. 

[tests last updated 2024-03-07]

| dataset name                  | resolution     | dataset version                    | test result    | link                          |
|-------------------------------|----------------|------------------------------------|----------------|-------------------------------|
| Daymet                        | ~ 1km          | version 4, downloaded 2023-01-24   | passed         | https://daymet.ornl.gov/
| Gridmet                       | ~ 4km          | 2023-01-31                         | passed         | https://www.climatologylab.org/gridmet.html |
| nclimgrid                     | ~ 5km           | downloaded 2024-03-01              | passed         | https://www.ncei.noaa.gov/products/land-based-station/nclimgrid-daily |
| downscaled CMIP6-WRF          | ~ 4km           | downloaded 2024-02-08              | passed         | https://climate.umn.edu/MN-CliMAT |