GRID 620 688 -125045.0 2246285.0 1000.0
BASE_PROJECTION_DEFINITION +proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23.0 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs

# MODULE SPECIFICATION
-------------------------

INTERCEPTION_METHOD              BUCKET
EVAPOTRANSPIRATION_METHOD        HARGREAVES
RUNOFF_METHOD                    CURVE_NUMBER
SOIL_MOISTURE_METHOD             FAO56_TWO_STAGE
PRECIPITATION_METHOD             GRIDDED
FOG_METHOD                       NONE
FLOW_ROUTING_METHOD              NONE
IRRIGATION_METHOD                FAO56
CROP_COEFFICIENT_METHOD          FAO56
ROOTING_DEPTH_METHOD             FAO56
DIRECT_NET_INFILTRATION_METHOD   NONE
DIRECT_SOIL_MOISTURE_METHOD      NONE
SOIL_STORAGE_MAX_METHOD          TABLE

# ---------- CMIP6 NetCDF climate files -----------------------
PRECIPITATION NETCDF historical_1995-2014_MIROC-ES2L__time_in_days__14-day.nc
PRECIPITATION_GRID_PROJECTION_DEFINITION +proj=latlon +datum=WGS84 
PRECIPITATION_NETCDF_Z_VAR             PREC_biasadju
PRECIPITATION_NETCDF_X_VAR                       lon
PRECIPITATION_NETCDF_Y_VAR                       lat
PRECIPITATION_NETCDF_TIME_VAR                   time
### SCALE FACTOR WHACKINESS: netCDF values are in mm per 3 hour period
###                          must convert from mm to inches (divide by 25.4) and multiply by 8
PRECIPITATION_SCALE_FACTOR                0.31496063     
PRECIPITATION_MISSING_VALUES_CODE            -9.e+33
PRECIPITATION_MISSING_VALUES_OPERATOR             <=
PRECIPITATION_MISSING_VALUES_ACTION             zero

TMAX NETCDF historical_1995-2014_MIROC-ES2L__time_in_days__14-day.nc
TMAX_GRID_PROJECTION_DEFINITION +proj=latlon +datum=WGS84
TMAX_NETCDF_Z_VAR            T2max_biasadju
TMAX_NETCDF_X_VAR                       lon
TMAX_NETCDF_Y_VAR                       lat
TMAX_NETCDF_TIME_VAR                   time
TMAX_UNITS_KELVIN
TMAX_MISSING_VALUES_CODE             -9.e+33
TMAX_MISSING_VALUES_OPERATOR             <=
TMAX_MISSING_VALUES_ACTION             mean

TMIN NETCDF historical_1995-2014_MIROC-ES2L__time_in_days__14-day.nc
TMIN_GRID_PROJECTION_DEFINITION +proj=latlon +datum=WGS84
TMIN_NETCDF_Z_VAR            T2min_biasadju
TMIN_NETCDF_X_VAR                       lon
TMIN_NETCDF_Y_VAR                       lat
TMIN_NETCDF_TIME_VAR                   time
TMIN_UNITS_KELVIN
TMIN_MISSING_VALUES_CODE            -9.e+33
TMIN_MISSING_VALUES_OPERATOR             <=
TMIN_MISSING_VALUES_ACTION             mean

# -------------------------------------------------------

AVAILABLE_WATER_CONTENT ARC_GRID AWS_grid_MN__1000m.asc
AVAILABLE_WATER_CONTENT_PROJECTION_DEFINITION +proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23.0 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs

LAND_USE ARC_GRID NLCD1992__1000m.asc
LAND_USE_PROJECTION_DEFINITION +proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23.0 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs

HYDROLOGIC_SOILS_GROUP ARC_GRID HSG_grid_MN__1000m.asc
HYDROLOGIC_SOILS_GROUP_PROJECTION_DEFINITION +proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23.0 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs

IRRIGATION_MASK CONSTANT 1.0

INITIAL_CONTINUOUS_FROZEN_GROUND_INDEX   CONSTANT  100.0
UPPER_LIMIT_CFGI 83.
LOWER_LIMIT_CFGI 55.

GROWING_SEASON 133 268 TRUE

INITIAL_PERCENT_SOIL_MOISTURE            CONSTANT  70.0
INITIAL_SNOW_COVER_STORAGE               CONSTANT   0.0

LAND_USE_LOOKUP_TABLE LU_lookup_MN_v3.txt
IRRIGATION_LOOKUP_TABLE IRR_lookup_MN_v3.txt

# Output options
#---------------
#OUTPUT ENABLE snowmelt snow_storage
#OUTPUT DISABLE snowfall runon rainfall 
OUTPUT DISABLE soil_storage delta_soil_storage surface_storage infiltration
OUTPUT DISABLE irrigation runon 
OUTPUT ENABLE gross_precip runoff_outside reference_ET0 actual_et
OUTPUT ENABLE rejected_net_infiltration net_infiltration runoff snowmelt tmax tmin

START_DATE 01/01/2000
END_DATE 01/14/2000

