

def calculate_potential_snowmelt(tmean_c: float,
                                 tmax_c: float) -> float:
    """Calculate the potential for snowmelt based on a simple index method.

    This simple algorithm is drawn from the original work by Wes Dripps (2003), in the code associated 
    with Appendix E of his dissertaion. 

    Args:
        tmean_c (float): daily mean air temperature, in degrees Celsius
        tmax_c (float): daily maximum air temperature, in degrees Celsius

    Returns:
        float: potential snowmelt, in millimeters of water
    """

    MELT_INDEX = 1.5         # mm potential melt per degree C
    FREEZING_PT_DEG_C = 0.0  # freezing point of water in degrees C

    if tmean_c > FREEZING_PT_DEG_C:
        potential_snowmelt = MELT_INDEX * tmax_c
    else:
        potential_snowmelt = 0.

    return potential_snowmelt

def references():
    """
    Dripps, W.R., 2003, The spatial and temporal variability of groundwater recharge within the Trout Lake 
    basin of northern Wisconsin: ProQuest Dissertations and Theses. 

    """
    pass