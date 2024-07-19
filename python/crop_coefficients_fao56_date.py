import numpy as np
import datetime as dt

def update_crop_coefficient_date_as_threshold(planting_date: dt.datetime,
                                              l_ini: int,
                                              l_dev: int,
                                              l_mid: int,
                                              l_late: int,
                                              l_fallow: int,
                                              kcb_min: float,
                                              kcb_mid: float,
                                              kcb_end: float,
                                              current_date: int):
    """Update crop coefficient given the current day of year.

    Args:
        planting_date (datetime): _description_
        l_ini (int): _description_
        l_dev (int): _description_
        l_mid (int): _description_
        l_late (int): 
        kcb_min (float): _description_
        kcb_mid (float): _description_
        kcb_kcb_end (float): _description_
        current_doy (int): _description_

                                    kcb_mid
                            /----------------------\
                           /                        \
                          /                          \
                         /                            \
                        /                              \
                       /                                \
                      /                                  \
        kcb_ini      /                                    \      kcb_end
    ----------------/                                      \----------------
  doy_plant
    |               |       |                      |       |                |
        l_ini         l_dev           l_mid          l_late     l_fallow

    """
    planting_month = planting_date.timetuple().tm_month
    planting_day = planting_date.timetuple().tm_day
    current_year = current_date.timetuple().tm_year
    current_doy = current_date.timetuple().tm_yday

    planting_doy = dt.date(current_year, planting_month, planting_day).timetuple().tm_yday

    doy_end_ini = current_doy + l_ini
    doy_end_dev = doy_end_ini + l_dev
    doy_end_mid = doy_end_dev + l_mid
    doy_end_late = doy_end_mid + l_late
    doy_end_fallow = doy_end_late + l_fallow

    if current_doy > doy_end_fallow:
        # TODO: possibly interpolate between kcb_end and kcb_min during l_fallow period
        kcb = kcb_min
    elif current_doy > doy_end_late:
        kcb = kcb_end
    elif current_doy > doy_end_mid:
        frac = ( current_doy - doy_end_mid ) / ( doy_end_late - doy_end_mid )
        kcb = kcb_mid * (1.0 - frac) + kcb_end * frac
    elif current_doy > doy_end_dev:
       kcb = kcb_mid
    elif current_doy > doy_end_ini:
        frac = ( current_doy - doy_plant ) / ( doy_end_dev - doy_plant )
        kcb = kcb_ini * (1.0 - frac) + kcb_mid * frac
    else:
       kcb = kcb_min

    return kcb


def calculate_kcb_max(wind_speed_meters_per_sec: float,
                      relative_humidity_min_pct: float,
                      kcb: float,
                      plant_height_meters: float):
    """Adjust the maximum crop coefficient (Kcb) to account for wind speed and relative humidity.

    Args:
        wind_speed_meters_per_sec (float): wind speed (meters per sec)
        relative_humidity_min_pct (float): relative humidity (percent, 0-100)
        kcb (float): crop coefficient (unitless)
        plant_height_meters (float): plant height (meters)

    Returns:
        float: adjusted crop coefficient (unitless)
    """
  
    # limits are suggested on page 123 of FAO-56 with respect to modifying the mid-season kcb
    rhmin = np.clip( relative_humidity_min_pct, a_min=[20.], a_max=[80.])
    u2 = np.clip(wind_speed_meters_per_sec, a_min=[1.], a_max=[6.])
    plant_height = np.clip(plant_height_meters, a_min=[1.], a_max=[10.])

    # equation 72, FAO-56, p 199
    kcb_max = np.max(1.2 + ( (0.04 * (u2 - 2.)
                            - 0.004 * (rhmin - 45.) ) ) 
                                    * (plant_height_meters/3.)**0.3, 
                     kcb + 0.05 )

    return kcb_max
