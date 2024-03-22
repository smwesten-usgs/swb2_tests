import numpy as np
import datetime as dt
import pandas as pd
import sys

import actual_et_fao56_two_stage as fao

class SWBCell__FAO56(SWBCell):

    def __init__(self,
                 latitude: float, 
                 available_water_capacity: float,
                 rooting_depth: float, 
                 calculation_method: str ='fao56',
                 kcb_min: float, 
                 kcb_mid: float, 
                 kcb_late: float, 
                 l_ini: float,
                 l_dev: float, 
                 l_mid:float, 
                 l_late: float, 
                 planting_date:dt.datetime ):

        super().__init__(latitude, available_water_capacity, rooting_depth, calculation_method='fao56',
                         thornthwaite_mather_df=None)

        self.kcb_min = kcb_min
        self.kcb_mid = kcb_mid
        self.kcb_late = kcb_late
        self.l_ini = l_ini
        self.l_dev = l_dev
        self.l_mid = l_mid
        self.l_late = l_late
        self.planting_date = planting_date
        self.planting_doy = (self.planting_date - dt.datetime(self.planting_date.year, 1, 1)).days + 1.
        # dev_doy: day of year that the kcb curve begins its climb from k_ini to k_mid
        self.dev_doy = self.planting_doy + self.l_ini
        # mid_doy: day of year that the kcb curve levels off at kcb_mid
        self.mid_doy = self.planting_doy + self.l_ini + self.l_dev
        # late_doy: day of year that the kcb curve begins to fall toward kcb_late
        self.late_doy = self.planting_doy + self.l_ini + self.l_dev + self.l_mid


    def init_swb_cell(self):
        self.init_soil_storage_max()
        self.init_soil_storage()
        self.apwl = 0.0

    def update_kcb(self,
                   kcb_min: float,
                   kcb_mid: float,
                   kcb_late: float,
                   l_ini: float,
                   l_dev: float,
                   l_mid: float,
                   l_late: float,
                   planting_date: dt.datetime,
                   current_date: dt.datetime,
                   day_of_year: int ):
        
        month = int(current_date.date.month)
        day = int(current_date.date.day)
        


    def calc_cell_water_budget(self, year, month, day, tmin_c, tmax_c, tmean_c, precip_mm):
        self.update_date_measures(year, month, day)
        self.update_daily_precip(precip_mm)
        self.update_daily_air_temps(tmin_c, tmax_c, tmean_c)
        self.calc_daily_pet()
#        self.partition_daily_precip()
        (self.rainfall, self.snowfall) = partition_daily_precip(self.gross_precip, self.tmin_c, self.tmax_c, self.tmean_c)
        self.potential_snowmelt = calculate_potential_snowmelt(self.tmean_c, self.tmax_c)
        self.update_snow_storage()
        self.previous_soil_storage = self.soil_storage
        self.previous_apwl = self.apwl

        (self.p_minus_pet, self.aet) = calculate_actual_et_fao56_two_stage(
                                                      self.rainfall,
                                                      self.snowmelt,
                                                      self.pet,
                                                      self.previous_soil_storage,
                                                      self.soil_storage_max)

        self.soil_storage = self.soil_storage + self.rainfall + self.snowmelt - self.aet

        self.calc_net_infiltration()



def references():
    """
    Alley, W.M., 1984, On the Treatment of Evapotranspiration, Soil Moisture Accounting, and Aquifer Recharge in Monthly
        Water Balance Models: Water Resources Research, v. 20, no. 8, p. 1137–1149.

    """
