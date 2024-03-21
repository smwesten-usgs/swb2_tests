import numpy as np

def calc_actual_et(rainfall, snowmelt, pet, soil_storage, soil_storage_max):
    """
    Return the current soil moisture (in inches) given the current soil moisture maximum,
    and the difference between (rainfall + snowmelt) minus the daily potential evapotranspiration.

    rainfall                Daily rainfall amount (mm or inches).
    snowmelt                Daily snowmelt amount (mm or inches).
    pet                     Potential evapotranspiration (mm).
    soil_storage   
    soil_storage_max        Maximum moisture content of a soil at field capacity.
    """

    p_minus_pet = rainfall + snowmelt - pet

    if p_minus_pet >= 0:
        # see Alley, 1984, eqn. 1
        aet = pet
    else:
        # see Alley, 1984, eqn 2.
        temp_soil_storage = soil_storage * np.exp( p_minus_pet / soil_storage_max )
        aet = soil_storage - temp_soil_storage


    return(p_minus_pet, aet)


def actual_et_references():
    """
    Alley, W.M., 1984, On the Treatment of Evapotranspiration, Soil Moisture Accounting, and Aquifer Recharge in Monthly
        Water Balance Models: Water Resources Research, v. 20, no. 8, p. 1137–1149.

    Thornthwaite, C.W., and Mather, J.R., 1957, Instructions and tables for computing potential evapotranspiration
        and the water balance: Publications in Climatology, v. 10, no. 3, p. 1-104.
    """
    pass