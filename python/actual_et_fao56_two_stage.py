"""
This module contains functions for calculating actual ET values by means of the
FAO-56 methodology. The citation for this publication is:

Allen, R.G., Pereira, L.S., Raes, D., and Smith, M., 1998, Crop evapotranspiration-Guidelines 
for computing crop water requirements-FAO Irrigation and drainage paper 56: Food and 
Agriculture Organization of the United Nations, Rome, 333 p.

"""

import numpy as np

def adjust_depletion_fraction_p(depletion_fraction: float, reference_et_mm: float):
    """Adjust the depletion fraction based on the value of the reference et.

       From FAO-56: "The fraction p is a function of the evaporation power of the atmosphere.
       At low rates of ETc, the p values listed in Table 22 are higher than at high rates of ETc.
       For hot dry weather conditions, where ETc is high, p is 10-25% less than the values
       presented in Table 22, and the soil is still relatively wet when the stress starts to occur.
       When the crop evapotranspiration is low, p will be up to 20% more than the listed values."

       Equation is from footnote 2, Table 22, p. 163.

    Returns:
        float: adjusted depletion fraction
    """
    p = depletion_fraction + 0.04 * (5.0 - reference_et_mm)

    return p


def update_evaporable_water_storage(evaporable_water_storage: float,
                                    evaporable_water_deficit: float,
                                    infiltration: float,
                                    total_evaporable_water_tew: float):
   
    """Update the soil evaporable water storage reservior.

       This is a simple methods that attempts to track readily evaporable water
       for use in later steps where evaporation from soil is calculated. 
    """

    evaporable_water_storage = np.clip(evaporable_water_storage + infiltration, a_min=0.0, a_max=total_evaporable_water_tew)
    evaporable_water_deficit = np.max(0.0, total_evaporable_water_tew - evaporable_water_storage)

    return evaporable_water_storage, evaporable_water_deficit


def calculate_evaporation_reduction_coefficient_kr(total_evaporable_water_tew: float,
                                                   readily_evaporable_water_rew: float,
                                                   evaporable_water_deficit: float):
   
    cond_def_le_rew = evaporable_water_deficit <= readily_evaporable_water_rew
    cond_def_lt_tew = evaporable_water_deficit < total_evaporable_water_tew

    kr = np.where(cond_def_le_rew, 
                  1.0,
                  np.where(cond_def_lt_tew,
                          (total_evaporable_water_tew - evaporable_water_deficit) /
                          (total_evaporable_water_tew - readily_evaporable_water_rew + 1.0e-8),
                          0.0)
    )
    return kr

def calculate_fraction_exposed_and_wetted_soil_fc(kcb_min: float,
                                                  kcb_mid: float,
                                                  kcb: float,
                                                  current_plant_height_m: float,
                                                  minimum_fraction_covered_soil: float):
    """Calculate the fraction of exposed and wetted soil based using the 
       current kcb value as a proxy for the current growth status.

       Assumption is that the exposed and wetted fraction decreases 
       through the growing season in lockstep with the value of the
       crop coefficient curve.

       Implemented as equation 76, FAO-56, Allen and others.

    Args:
        kcb_min (float): minimum kcb value from table
        kcb_mid (float): mid-season kcb value from table
        kcb (float): current kcb value
        current_plant_height_m (float): current plant height in meters
        minimum_fraction_covered_soil (float): minimum expected fraction of covered soil

    Returns:
        float: fraction of exposed and wetted soil
    """

    numerator = np.max(kcb - kcb_min, 0.0)
    denominator = kcb_mid - kcb_min
    exponent = 1.0 + 0.5 * current_plant_height

    fc = np.where(denominator > 0,
                 (numerator / denominator)^exponent,
                 1.0
                 )
   
    fc = np.max(fc, minimum_fraction_covered_soil)
    fraction_exposed_and_wetted_soil_few = np.clip(1.0 - fc, a_min=0.05, a_max=1.0)

    return fraction_exposed_and_wetted_soil_few


def calculate_surface_evap_coefficient_ke(kcb_max: float,
                                          kcb: float,
                                          evaporation_reduction_coefficient_kr: float,
                                          fraction_exposed_and_wetted_soil_few: float):
    """This function estimates Ke, the bare surface evaporation coefficient
       Implemented as equation 71, FAO-56, Allen and others
       
    Args:
        kcb_max (float): maximum crop coefficient table value
        kcb (float): current crop coefficient
        evaporation_reduction_coefficient_kr (float): evaporation reduction coefficient
        fraction_exposed_and_wetted_soil_few (float): fraction of exposed and wetted soil

    Returns:
        float: evaporation coefficient ke
    """
   
    maximum_value = np.min(1.0, fraction_exposed_and_wetted_soil_few * kcb_max)
    evaporation_coefficient_ke = np.min(evaporation_reduction_coefficient_kr 
                                         * (kcb_max - kcb_min),
                                       maximum_value)
    return evaporation_coefficient_ke


def calculate_total_available_water(adjusted_depletion_fraction_p: float,
                                    current_rooting_depth: float,
                                    available_water_capacity: float):
    """This subroutine updates the total available water (TAW)
       (water within the rootzone)

       This was originally designed with Imperial units in mind. So the 
       current rooting depth would be in feet; the available water
       capacity would be in inches per foot. The resulting total available 
       water would then be in inches. One should be able to specify rooting
       depth in meters, and the available water capacity in terms of 
       millimeters per meter.

    Args:
        adjusted_depletion_fraction_p (float): adjusted depletion fraction
        current_rooting_depth (float): current rooting depth
        available_water_capacity (float): available water capacity
    """

    total_available_water_taw = current_rooting_depth * available_water_capacity
    readily_available_water_raw = adjusted_depletion_fraction_p * total_available_water_taw

    return total_available_water_taw, readily_available_water_raw



def update_plant_height(kcb_min: float, 
                        kcb_mid: float,
                        kcb: float,
                        mean_plant_height_m: float):
    
    """Update the plant height by scaling values relative to the 
       position of the current Kcb value on the Kcb curve

    Returns:
        float: current plant height in meters
    """
    plant_height_minimum_m = 0.1

    numerator = kcb - kcb_min
    denominator = kcb_mid - kcb_min

    current_plant_height = np.where(kcb > kcb_min,
                           np.clip(numerator / denominator * mean_plant_height_m, a_min=plant_height_minimum_m, a_max=mean_plant_height_m),
                           plant_height_minimum_m)
    
    return current_plant_height


def calculate_water_stress_coefficient_ks(total_available_water_taw: float,
                                          readily_available_water_raw: float,
                                          soil_moisture_deficit: float):
    """Estimate Ks, water stress coefficient.
       Implemented as equation 84, FAO-56, Allen and others.

    Args:
        total_available_water_taw (float): total available water
        readily_available_water_raw (float): readily available water
        soil_moisture_deficit (float): soil moisture deficit

    Returns:
        float: water stress coefficient
    """
   
    cond_def_le_raw = soil_moisture_deficit <= readily_available_water_raw
    cond_def_lt_taw = soil_moisture_deficit < total_available_water_taw

    ks = np.where(cond_def_le_raw, 
                  1.0,
                  np.where(cond_def_lt_taw,
                          (total_available_water_taw - soil_moisture_deficit) /
                          (total_available_water_taw - readily_available_water_raw + 1.0e-8),
                          0.0)
    )
    return ks
