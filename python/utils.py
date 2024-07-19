import numpy as np
import datetime as dt

def update_moving_average(previous_average, new_value, num_days=30):

    k = 2 / (num_days + 1)

    new_average = k * ( new_value - previous_average ) + previous_average

    return new_average
    
def date_to_doy(date_value: dt.date):

    doy = date_value.timetuple().tm_yday
    return doy
