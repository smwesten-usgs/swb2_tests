import numpy as np

def update_growing_degree_day(tmin: float,
                              tmax: float,
                              gdd_base: float = 10.,
                              gdd_max: float = 30.):
    """_summary_

    Args:
        tmin (float): minimum daily air temperature, in degrees Celsius
        tmax (float): maximum daily air temperature, in degrees Celsius
        gdd_base (float, optional): base temperature below which GDD does not accumulate. Defaults to 10.
        gdd_max (float, optional): maximum temperature to cap daily GDD accumulation. Defaults to 30.

    Returns:
        float: Growing degree day increment
    """
    min_temps = np.where(tmin > gdd_base, tmin, gdd_base)
    max_temps = np.where(tmax < gdd_max, tmax, gdd_max )
    mean_temps = (min_temps + max_temps) / 2.0

    gdd_increment = np.where(mean_temps > gdd_base,
                             mean_temps - gdd_base,
                             0.0)
    
    return gdd_increment