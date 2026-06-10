GRID 6 6 0.0 0.0 100.0
BASE_PROJECTION_DEFINITION +proj=tmerc +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs

# MODULE SPECIFICATION
-------------------------

INTERCEPTION_METHOD              BUCKET
EVAPOTRANSPIRATION_METHOD        HARGREAVES
RUNOFF_METHOD                    CURVE_NUMBER
SOIL_MOISTURE_METHOD             THORNTHWAITE-MATHER
PRECIPITATION_METHOD             TABULAR
FOG_METHOD                       NONE
FLOW_ROUTING_METHOD              D8
IRRIGATION_METHOD                NONE
CROP_COEFFICIENT_METHOD          NONE
GROWING_DEGREE_DAY_METHOD        MODIFIED_GROWING_DEGREE-DAY
ROOTING_DEPTH_METHOD             STATIC
DIRECT_NET_INFILTRATION_METHOD   NONE
DIRECT_SOIL_MOISTURE_METHOD      NONE
SOIL_STORAGE_MAX_METHOD          CALCULATED
AVAILABLE_WATER_CONTENT_METHOD   GRIDDED

# Gridded input files
# -----------------------------------------------
FLOW_DIRECTION ARC_GRID d8_flow_direction__6x6.asc

LAND_USE CONSTANT 1

HYDROLOGIC_SOILS_GROUP CONSTANT 1

AVAILABLE_WATER_CONTENT CONSTANT 3.5

# Miscellaneous inputs
# ---------------------------------------------------
INITIAL_CONTINUOUS_FROZEN_GROUND_INDEX CONSTANT 0.0
CFGI_UPPER_LIMIT CONSTANT 83.
CFGI_LOWER_LIMIT CONSTANT 55.

GROWING_SEASON 133 268 TRUE

INITIAL_PERCENT_SOIL_MOISTURE CONSTANT 50.0
INITIAL_SNOW_COVER_STORAGE CONSTANT 0.0

# Lookup Tables
# -------------------------------------------
LAND_USE_LOOKUP_TABLE LU_lookup_d8_test.txt
WEATHER_DATA_LOOKUP_TABLE weather_data_d8_test.txt

# Output options
#---------------
OUTPUT ENABLE runoff runon runoff_outside rainfall gross_precip
OUTPUT ENABLE actual_et net_infiltration soil_storage delta_soil_storage
OUTPUT DISABLE snowfall snowmelt snow_storage tmin tmax reference_ET0
OUTPUT DISABLE surface_storage infiltration

# Dump all cells by dumping a representative cell
DUMP_VARIABLES COORDS 250 250 ID d8_test_cell

START_DATE 06/01/2000
END_DATE 06/14/2000
