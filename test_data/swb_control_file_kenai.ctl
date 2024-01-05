! create grid centered on Kenai Airport
! grid definition: projected coordinates are EPSG 3338, meters
!      nx    ny       xll          yll     resolution
GRID   1      1    150243      1179206            250
BASE_PROJECTION_DEFINITION +proj=aea +lat_0=50 +lon_0=-154 +lat_1=55 +lat_2=65 +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs

%% Define methods
-----------------

INTERCEPTION_METHOD              BUCKET
EVAPOTRANSPIRATION_METHOD        HARGREAVES
RUNOFF_METHOD                    CURVE_NUMBER
SOIL_MOISTURE_METHOD             THORNTHWAITE-MATHER
PRECIPITATION_METHOD             TABULAR
FOG_METHOD                       NONE
FLOW_ROUTING_METHOD              NONE
IRRIGATION_METHOD                NONE  #NONE turns off all irrigation  #FAO-56 uses that method
ROOTING_DEPTH_METHOD             NONE
CROP_COEFFICIENT_METHOD          NONE  #Used to calculate actual ET with soil moisture
DIRECT_RECHARGE_METHOD           NONE
SOIL_STORAGE_MAX_METHOD          CALCULATED
AVAILABLE_WATER_CONTENT_METHOD   GRIDDED

%% define location, projection, and conversions for weather data
----------------------------------------------------------------

INITIAL_CONTINUOUS_FROZEN_GROUND_INDEX CONSTANT 100.0
UPPER_LIMIT_CFGI 83.
LOWER_LIMIT_CFGI 55.

%% specify location and projection for input GIS grids
------------------------------------------------------

HYDROLOGIC_SOILS_GROUP CONSTANT 1

LAND_USE CONSTANT 1

%% 3.6 inches per foot equal 300 mm/m
AVAILABLE_WATER_CONTENT CONSTANT 3.6

%% specify location and names for all lookup tables
---------------------------------------------------
LAND_USE_LOOKUP_TABLE LU_Lookup_Test.tsv
WEATHER_DATA_LOOKUP_TABLE daily_weather_data__Kenai_Apt_thru_2014_w_Soldotna_thru_2023_corrected_date.txt

%% initial conditions for soil moisture and snow storage amounts
%% may be specified as grids, but using a constant amount and
%% allowing the model to "spin up" for a year is also acceptable.

INITIAL_PERCENT_SOIL_MOISTURE CONSTANT 100.0
INITIAL_SNOW_COVER_STORAGE CONSTANT 0.0


%% OUTPUT CONTROL SECTION:
OUTPUT DISABLE snow_storage
OUTPUT DISABLE tmin tmax reference_ET0 bare_soil_evaporation crop_et
OUTPUT DISABLE soil_storage delta_soil_storage 
OUTPUT DISABLE runon soil_storage delta_soil_storage
OUTPUT DISABLE snowfall net_infiltration irrigation

OUTPUT DISABLE gross_precipitation interception 
OUTPUT DISABLE runoff_outside rejected_net_infiltration 
OUTPUT ENABLE runoff actual_et rainfall snowmelt 

# approximate coordinates for Kenai Municipal Airport
DUMP_VARIABLES COORDINATES 150393 1179331 ID Kenai_Airpt

%% start and end date may be any valid dates in SWB version 2.0
%% remember to allow for adequate model spin up; running the
%% model for just a month or two will give questionable results

START_DATE 01/01/1967
END_DATE 12/31/1970