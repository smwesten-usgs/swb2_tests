import numpy as np
import datetime as dt
import pandas as pd
import sys

import actual_et_fao56_two_stage as fao
import crop_coefficients_fao56_date as cc
from swb_cell import SWBCell

class SWBCell__FAO56(SWBCell):

    def __init__(self,
                 latitude: float, 
                 available_water_capacity: float,
                 rooting_depth: float, 
                 calculation_method: str,
                 kcb_min: float, 
                 kcb_mid: float, 
                 kcb_late: float, 
                 l_ini: float,
                 l_dev: float, 
                 l_mid:float, 
                 l_late: float, 
                 l_fallow: float,
                 planting_date:dt.datetime,
                 mean_plant_height: float):

        super().__init__(latitude, available_water_capacity, rooting_depth, calculation_method='fao56',
                         thornthwaite_mather_df=None)

        self.kcb_min = kcb_min
        self.kcb_mid = kcb_mid
        self.kcb_late = kcb_late
        self.l_ini = l_ini
        self.l_dev = l_dev
        self.l_mid = l_mid
        self.l_late = l_late
        self.l_fallow = l_fallow
        self.planting_date = planting_date
        self.mean_plant_height = mean_plant_height


    def init_swb_cell(self):
        self.init_soil_storage_max()
        self.init_soil_storage()
        self.apwl = 0.0


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

        (self.p_minus_pet, self.aet) = fao.calculate_actual_et_fao56_two_stage(
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
