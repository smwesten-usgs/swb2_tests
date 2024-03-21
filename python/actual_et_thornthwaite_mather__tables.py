import numpy as np
import pandas as pd 
from scipy.optimize import curve_fit
from numpy import exp, log

TM_SLOPE_TERM_IN      = 0.478769194198665
TM_SLOPE_TERM_MM      = 0.539815721014123
TM_EXPONENT_TERM      = -1.03678439421169

def init__tm_tables(table_path):
    tm = pd.read_csv(table_path)
    return tm

def thornthwaite_mather_soil_moisture_millimeters(max_soil_moisture, apwl):
    """
    Return the current soil moisture (in millimeters) given the current soil moisture maximum (in millimeters),
    as well as the current accumulated potential water loss (APWL). APWL is the running sum of the difference
    between the potential ET and the actual ET. Equation and constants come from an R equation fitting exercise 
    applied to the original soil-mosture retention tables included in Thornthwaite and Mather (1957).

    max_soil_moisture       Maximum moisture content of a soil at field capacity, in millimeters.
    apwl                    Running sum of daily difference between PET and AET, in millimeters.
    """

    soil_moisture = np.where( max_soil_moisture > 0.,
        max_soil_moisture * 10**(-TM_SLOPE_TERM_MM*apwl*max_soil_moisture**TM_EXPONENT_TERM),
        0.0
    )
    return(soil_moisture)

def thornthwaite_mather_accumulated_potential_water_loss_millimeters(max_soil_moisture, soil_moisture):
    """
    Return the accumulated potential water loss (in millimeters) given the current soil moisture (in millimeters),
    as well as maximum soil moisture (in millimeters). APWL is the running sum of the difference
    between the potential ET and the actual ET. Equation and constants come from an R equation fitting exercise 
    applied to the original soil-mosture retention tables included in Thornthwaite and Mather (1957).    
    """
    apwl = np.where(max_soil_moisture > 0.,
        - (np.log(soil_moisture) - np.log(max_soil_moisture))/(np.log(10)*TM_SLOPE_TERM_MM*max_soil_moisture**TM_EXPONENT_TERM),
        0.0
        )
    return(apwl)


def plotit(x, y, func_y):
    fig, ax = plt.subplots(1,1,figsize=(12, 8),sharex=False)
    ax.plot(x, y, marker='.', linestyle=' ', color='blue', markersize=4, label='TM Table values')
    ax.plot(x, func_y, marker=' ', linestyle='-', 
            color='red', linewidth=1., label='TM function')
    ax.legend()


def calc_actual_et__tm_eqns(rainfall, snowmelt, pet, previous_apwl, soil_storage):
    """
    Return the current soil moisture (in mm) given the current soil moisture maximum,
    and the difference between (rainfall + snowmelt) minus the daily potential evapotranspiration.

    This is not a general function. It has been written specifically to make the actual ET calculation
    for a soil reservoir size of 300mm. The purpose of this code is to verify similar output between the
    exponential decay function (Alley, 1984) and calculations made with the Thornthwaite-Mather soil-moisture
    retention tables given in THornthwaite and Mather (1957).

    rainfall                Daily rainfall amount (mm).
    snowmelt                Daily snowmelt amount (mm).
    pet                     Potential evapotranspiration (mm).
    previous_apwl           Previous timestep's accumulated potential water loss (mm).
    soil_storage            Amount of moisture in soil storage reservoir (mm)   
    tm_df                   Thornthwaite-Mather soil moisture retention values from Table 10, 
                            Thornthwaite and Mather (1957). Pandas dataframe.
    """

    p_minus_pet = rainfall + snowmelt - pet

    if p_minus_pet >= 0:

        # update soil moisture amount with P - PET; back-calculate a new APWL value from the 
        # updated soil moisture amount

        # alert!! this entire function is hardwired to work *only* with the 300mm soil moisture tables
        temp_soil_storage = np.min((300., soil_storage + p_minus_pet))
        apwl = thornthwaite_mather_accumulated_potential_water_loss_millimeters(300., temp_soil_storage)
        aet = pet
    else:

        # update apwl; look up resulting soil moisture value
        # apwl terms are positive in the tables

        # Thornthwaite notes that: "Since the values of P-PE are not accumulated as in the case of monthly
        #                           calculations, it is necessary to accumulate them as the work is carried
        #                           out by finding the value of the soil moisture storage in the body of the
        #                           table and then counting ahead by a number equal to the value of P-PE to
        #                           obtain the new value of soil moisture storage.

        apwl_temp = thornthwaite_mather_accumulated_potential_water_loss_millimeters(300., soil_storage)
        apwl = apwl_temp + np.abs(p_minus_pet)
        #apwl = previous_apwl + np.abs(p_minus_pet)
        temp_soil_storage = thornthwaite_mather_soil_moisture_millimeters(300., apwl)

        aet = soil_storage - temp_soil_storage

    return(p_minus_pet, apwl, aet)



def calc_actual_et__tm_tables(rainfall, snowmelt, pet, previous_apwl, soil_storage, tm_df):
    """
    Return the current soil moisture (in inches) given the current soil moisture maximum,
    and the difference between (rainfall + snowmelt) minus the daily potential evapotranspiration.

    This is not a general function. It has been written specifically to make the actual ET calculation
    for a soil reservoir size of 300mm. The purpose of this code is to verify similar output between the
    exponential decay function (Alley, 1984) and calculations made with the Thornthwaite-Mather soil-moisture
    retention tables given in THornthwaite and Mather (1957).

    rainfall                Daily rainfall amount (mm).
    snowmelt                Daily snowmelt amount (mm).
    pet                     Potential evapotranspiration (mm).
    previous_apwl           Previous timestep's accumulated potential water loss (mm).
    soil_storage            Amount of moisture in soil storage reservoir (mm)   
    tm_df                   Thornthwaite-Mather soil moisture retention values from Table 10, 
                            Thornthwaite and Mather (1957). Pandas dataframe.
    """

    p_minus_pet = rainfall + snowmelt - pet

    if p_minus_pet >= 0:

        # update soil moisture amount with P - PET; back-calculate a new APWL value from the 
        # updated soil moisture amount

        # alert!! this entire function is hardwired to work *only* with the 300mm soil moisture tables
        temp_soil_storage = np.min((300., soil_storage + p_minus_pet))
        apwl = tm_df.iloc[(tm_df['sz_300_calc']-temp_soil_storage).abs().argsort()[:1]]['apwl_mm'].values[0]
        aet = pet
    else:

        # update apwl; look up resulting soil moisture value
        # apwl terms are positive in the tables

        # Thornthwaite notes that: "Since the values of P-PE are not accumulated as in the case of monthly
        #                           calculations, it is necessary to accumulate them as the work is carried
        #                           out by finding the value of the soil moisture storage in the body of the
        #                           table and then counting ahead by a number equal to the value of P-PE to
        #                           obtain the new value of soil moisture storage.

        apwl_temp = tm_df.iloc[(tm_df['sz_300_calc']-soil_storage).abs().argsort()[:1]]['apwl_mm'].values[0]

        apwl = apwl_temp + np.abs(p_minus_pet)
        temp_soil_storage = tm_df.iloc[(tm_df['apwl_mm']-apwl).abs().argsort()[:1]]['sz_300_calc'].values[0]

        aet = soil_storage - temp_soil_storage

    return(p_minus_pet, apwl, aet)


def actual_et__tm_tables_references():
    """
    Thornthwaite, C.W., and Mather, J.R., 1957, Instructions and tables for computing potential evapotranspiration
        and the water balance: Publications in Climatology, v. 10, no. 3, p. 1-104.
    """
    pass