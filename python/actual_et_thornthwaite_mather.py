import numpy as np

def calc_daily_soil_storage(rainfall, snowmelt, pet, previous_soil_storage, soil_storage_max,
                            truncate_values=False, round_values=False):
    """
    Return the current soil moisture (in inches) given the current soil moisture maximum,
    and the difference between (rainfall + snowmelt) minus the daily potential evapotranspiration.

    rainfall                Daily rainfall amount (mm or inches).
    snowmelt                Daily snowmelt amount (mm or inches).
    previous_soil_storage   
    soil_storage_max        Maximum moisture content of a soil at field capacity.
    """

    p_minus_pet = rainfall + snowmelt - pet

    if p_minus_pet >= 0:
        # see Alley, 1984, eqn. 1
        soil_storage = previous_soil_storage + p_minus_pet
        aet = pet
    else:
        # see Alley, 1984, eqn 2.

        # in order to come close to the published Thornthwaite-Mather tables, it seems to be
        # necessary to truncate or round the values, which is apparently what was done in the production
        # of the original tables

        if truncate_values:
            soil_storage = np.trunc( previous_soil_storage * np.exp( p_minus_pet / soil_storage_max ) )
            aet = np.trunc(previous_soil_storage - soil_storage)
        elif round_values:
            soil_storage = np.round(previous_soil_storage * 
                                    np.exp( np.round(p_minus_pet / soil_storage_max, decimals=3) ), decimals=0)
            aet = np.round(previous_soil_storage - soil_storage, decimals=0)
        else:
            soil_storage = previous_soil_storage * np.exp( p_minus_pet / soil_storage_max )
            aet = previous_soil_storage - soil_storage


    return(soil_storage, p_minus_pet, aet)


def actual_et_references():
    """
    Alley, W.M., 1984, On the Treatment of Evapotranspiration, Soil Moisture Accounting, and Aquifer Recharge in Monthly
        Water Balance Models: Water Resources Research, v. 20, no. 8, p. 1137–1149.

    Thornthwaite, C.W., and Mather, J.R., 1957, Instructions and tables for computing potential evapotranspiration
        and the water balance: Publications in Climatology, v. 10, no. 3, p. 1-104.
    """
    pass