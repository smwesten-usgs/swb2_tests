import numpy as np
import datetime as dt
import pandas as pd
import sys
from pet_hargreaves_samani import calculate_et0_hargreaves_samani
from actual_et_thornthwaite_mather import calc_actual_et
from actual_et_thornthwaite_mather__tables import (calc_actual_et__tm_tables,
                                                  calc_actual_et__tm_eqns)
from growing_degree_day import update_growing_degree_day
from partition_daily_precipitation import partition_daily_precip
from potential_snowmelt import calculate_potential_snowmelt

class SWBCell:

    def __init__(self, latitude, available_water_capacity, rooting_depth, calculation_method='tm_exp',
                 thornthwaite_mather_df=None):
        self.latitude = latitude
        self.available_water_capacity = available_water_capacity
        self.gross_precip = 0.
        self.rainfall = 0.
        self.snowmelt = 0.
        self.snowfall = 0.
        self.gdd = 0.
        self.snow_storage = 0.
        self.pet = 0.
        self.apwl = 0.
        self.rooting_depth = rooting_depth
        self.net_infiltration = 0.
        self.calc_method = calculation_method
        self.tm_df=thornthwaite_mather_df
        self.output_dict = {}

    def init_soil_storage_max(self):
        # rooting depth in meters, awc in mm/m
        self.soil_storage_max = self.rooting_depth * self.available_water_capacity


    def init_soil_storage(self, percent_soil_storage=100.):
        self.soil_storage = self.soil_storage_max * percent_soil_storage / 100.

    def update_date_measures(self, year, month, day):
        self.date = dt.datetime(year, month, day)
        self.day_of_year = (self.date - dt.datetime(year, 1, 1)).days + 1.
        self.number_of_days_in_year = (dt.datetime(year, 12, 31) - dt.datetime(year, 1, 1)).days + 1.
        self.dtindex = f'{self.date.year}{self.date.month:02d}{self.date.day:02d}'


    def update_daily_precip(self, precip_mm):
        self.gross_precip = precip_mm


    def update_snow_storage(self):
        self.snow_storage += self.snowfall 
        
        if self.snow_storage > self.potential_snowmelt:
          self.snowmelt = self.potential_snowmelt
          self.snow_storage = self.snow_storage - self.snowmelt
        else:   # not enough snowcover to satisfy the amount that *could* melt
          self.snowmelt = self.snow_storage
          self.snow_storage = 0.


    def update_daily_air_temps(self, tmin_c, tmax_c, tmean_c):
        self.tmin_c = tmin_c
        self.tmax_c = tmax_c
        self.tmean_c = tmean_c

    def update_daily_pet(self, pet):
        self.pet = pet


    def calc_daily_pet(self):
        self.pet = calculate_et0_hargreaves_samani(self.day_of_year, self.number_of_days_in_year, self.latitude,
                                        air_temp_min=self.tmin_c, air_temp_max=self.tmax_c, air_temp_mean=self.tmean_c)


    def calc_net_infiltration(self):
        if self.soil_storage > self.soil_storage_max:
            self.net_infiltration = self.soil_storage - self.soil_storage_max
            self.soil_storage = self.soil_storage_max
        else:
            self.net_infiltration = 0.

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
        self.previous_apwl = self.apwl

        if month == 1 and day == 1:
            self.gdd = 0.
        else:
            self.gdd += update_growing_degree_day(tmin=self.tmin_c,
                                                  tmax=self.tmax_c)

        if self.calc_method=='tm_table':
            (self.p_minus_pet, self.apwl, self.aet) = calc_actual_et__tm_tables(self.rainfall,
                                                                                self.snowmelt,
                                                                                self.pet,
                                                                                self.previous_apwl,
                                                                                self.previous_soil_storage,
                                                                                self.tm_df)

        elif self.calc_method=='tm_eqns':
            (self.p_minus_pet, self.apwl, self.aet) = calc_actual_et__tm_eqns (self.rainfall,
                                                                               self.snowmelt,
                                                                               self.pet,
                                                                               self.previous_apwl,
                                                                               self.previous_soil_storage)

        elif self.calc_method=='tm_exp':
            (self.p_minus_pet, self.aet) = calc_actual_et(self.rainfall,
                                                          self.snowmelt,
                                                          self.pet,
                                                          self.previous_soil_storage,
                                                          self.soil_storage_max)

        else:
            print("You need to choose an actual ET calculation method ('tm_tables', or 'tm_exp').")
            sys.exit(-1)

        self.soil_storage = self.soil_storage + self.rainfall + self.snowmelt - self.aet

        self.calc_net_infiltration()

    def variables_toscreen(self):
        print(f'{self.date}  {self.previous_soil_storage:.2f}  {self.soil_storage:.2f}  {self.rainfall:.2f}  {self.snowmelt:.2f}'
              f'  {self.pet:.2f}'
              f'  {self.p_minus_pet:.2f}  {self.aet:.2f}  {self.net_infiltration:.2f}')
        
    def variables_todict(self):
        self.output_dict[self.dtindex] = [self.date, self.previous_soil_storage, self.soil_storage,
                                          self.rainfall, self.snow_storage, self.snowfall, self.snowmelt,
                                          self.pet, self.p_minus_pet, self.aet, self.net_infiltration, self.apwl,
                                          self.gdd]
        
    def convert_dict_to_df(self):
        self.output_df = pd.DataFrame.from_dict(self.output_dict, orient='index')
        self.output_df.columns=['date','previous_soil_storage','soil_storage','rainfall',
                                'snow_storage', 'snowfall', 'snowmelt','pet','p_minus_pet',
                                'aet','net_infiltration','apwl','gdd']


def references():
    """
    Alley, W.M., 1984, On the Treatment of Evapotranspiration, Soil Moisture Accounting, and Aquifer Recharge in Monthly
        Water Balance Models: Water Resources Research, v. 20, no. 8, p. 1137–1149.

    """
