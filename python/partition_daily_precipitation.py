def partition_daily_precip(gross_precipitation: float,
                           tmin_c: float, 
                           tmax_c: float, 
                           tmean_c: float) -> tuple[float]:
    """Partition daily gross precipitation into rainfall and snowfall.

    This simple algorithm is drawn from the original work by Wes Dripps (2003), in the code associated 
    with Appendix E of his dissertaion. A threshold is established, and daily precipitation amounts are
    partitioned into 'rainfall' or 'snowfall' on the basis of this threshold.

    Args:
        gross_precipitation (float): gross precipitation, unitless
        tmin_c (float): daily minimum air temperature, in degrees Celsius
        tmax_c (float): daily maximum air temperature, in degrees Celsius
        tmean_c (float): daily mean air temperature, in degrees Celsius
    """
    def c_to_f(t):
        return t*1.8 + 32.

    # snowfall criteria from Wes Dripps (2003) code:
    # (dailytmp - (0.33 * (tmax - tmin))) <= 32 
    #

    FREEZING_PT_DEG_F = 32.0

    snowfall_threshold = c_to_f(tmean_c) - (c_to_f(tmax_c) - c_to_f(tmin_c)) / 3.

    if snowfall_threshold <= FREEZING_PT_DEG_F:
        snowfall = gross_precipitation
        rainfall = 0.
    else:
        snowfall = 0.
        rainfall = gross_precipitation

    return rainfall, snowfall

def references():
    """
    Dripps, W.R., 2003, The spatial and temporal variability of groundwater recharge within the Trout Lake 
    basin of northern Wisconsin: ProQuest Dissertations and Theses. 

    """
    pass