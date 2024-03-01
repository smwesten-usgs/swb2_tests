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

# ---------- Daymet NetCDF daily weather data files ------------------------
PRECIPITATION NETCDF gridmet_pr_2000_mn__14-day.nc
PRECIPITATION_GRID_PROJECTION_DEFINITION +proj=lonlat +ellps=WGS84 +datum=WGS84 +no_defs
PRECIPITATION_NETCDF_Z_VAR            precipitation_amount
PRECIPITATION_NETCDF_Y_VAR                             lat
PRECIPITATION_NETCDF_X_VAR                             lon
PRECIPITATION_NETCDF_TIME_VAR                          day
PRECIPITATION_UNITS_MILLIMETERS
PRECIPITATION_MISSING_VALUES_CODE                  -9999.0
PRECIPITATION_MISSING_VALUES_OPERATOR                   <=
PRECIPITATION_MISSING_VALUES_ACTION                   zero

TMAX NETCDF gridmet_tmmx_2000_mn__14-day.nc
TMAX_GRID_PROJECTION_DEFINITION +proj=lonlat +ellps=WGS84 +datum=WGS84 +no_defs
TMAX_NETCDF_Z_VAR                         air_temperature
TMAX_NETCDF_Y_VAR                                     lat
TMAX_NETCDF_X_VAR                                     lon
TMAX_NETCDF_TIME_VAR                                  day
TMAX_UNITS_KELVIN
TMAX_MISSING_VALUES_CODE                          -9999.0
TMAX_MISSING_VALUES_OPERATOR                           <=
TMAX_MISSING_VALUES_ACTION                           mean

TMIN NETCDF gridmet_tmmn_2000_mn__14-day.nc
TMIN_GRID_PROJECTION_DEFINITION +proj=lonlat +ellps=WGS84 +datum=WGS84 +no_defs
TMIN_NETCDF_Z_VAR                         air_temperature
TMIN_NETCDF_Y_VAR                                     lat
TMIN_NETCDF_X_VAR                                     lon
TMIN_NETCDF_TIME_VAR                                  day
TMIN_UNITS_KELVIN
TMIN_MISSING_VALUES_CODE                          -9999.0
TMIN_MISSING_VALUES_OPERATOR                           <=
TMIN_MISSING_VALUES_ACTION                           mean
# --------------------------------------------------------------------------

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
OUTPUT DISABLE snowmelt snow_storage
OUTPUT DISABLE snowfall runon rainfall 
OUTPUT DISABLE soil_storage delta_soil_storage surface_storage infiltration
OUTPUT DISABLE irrigation runon 
OUTPUT ENABLE gross_precip tmax tmin
OUTPUT_DISABLE runoff_outside reference_ET0 actual_et
OUTPUT DISABLE rejected_net_infiltration net_infiltration runoff snowmelt

START_DATE 01/01/2000
END_DATE 01/14/2000

