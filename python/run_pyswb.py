import pandas as pd
import matplotlib.pyplot as plt
import pathlib as pl
import sys
import subprocess

base_dir = str(pl.Path.cwd().parent)
python_script_dir = pl.Path.cwd().parent / 'python'
swb_work_dir = pl.Path.cwd().parent / 'swb_work'
logfile_dir = pl.Path.cwd().parent / 'logfiles'
test_data_dir = pl.Path.cwd().parent / 'test_data'
tm_table_file = test_data_dir / 'Thornthwaite_soil_moisture_retention_tables__millimeters.csv'
output_dir = pl.Path.cwd().parent / 'output'
swb2_executable = str(pl.Path.cwd().parent / 'bin' /'swb2.exe')
sys.path.append(str(python_script_dir))

from swb_cell import SWBCell
import run_management as rm

tm_soil_moisture_retention_df = pd.read_csv(tm_table_file)

rm.destroy_model_work_output_and_logfile_dirs(base_dir=base_dir,
                                              swb_work_dir=swb_work_dir,
                                              logfile_dir=logfile_dir,
                                              output_dir=output_dir)
rm.create_model_work_output_and_logfile_dirs(base_dir=base_dir,
                                             swb_work_dir=swb_work_dir,
                                             logfile_dir=logfile_dir,
                                             output_dir=output_dir)

dry_run = False
lookup_dir_arg_text = f"--lookup_dir={str(test_data_dir)}"
weather_data_dir_arg_text = f"--weather_data_dir={str(test_data_dir)}"
output_dir_arg_text = f"--output_dir={str(output_dir)}"
logfile_dir_arg_text = f"--logfile_dir={str(logfile_dir)}"
control_file_path = str(test_data_dir / 'swb_control_file_kenai.ctl')
output_prefix = '--output_prefix=swb_kenai_'

swb_arg_text = [swb2_executable, output_dir_arg_text, lookup_dir_arg_text, weather_data_dir_arg_text, output_prefix, logfile_dir_arg_text, control_file_path]

f = open("stdout.txt", "w")

if not dry_run:
  with rm.cd(swb_work_dir):
#    p = subprocess.Popen(swb_arg_text, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p = subprocess.Popen(swb_arg_text, stdout=f, stderr=subprocess.DEVNULL)
    p.wait()

swb_df = pd.read_csv(pl.Path(output_dir, 'SWB2_variable_values__Kenai_Airpt__col_1__row_1__x_150393__y_1179331.csv'))
# eliminate pesky spaces around column names
swb_df.columns = swb_df.columns.str.replace(' ', '')

swb_df['tminf'] = swb_df.loc[:,'tmin']
swb_df['tmaxf'] = swb_df.loc[:,'tmax']
swb_df['tmeanf'] = swb_df.loc[:,'tmean']
swb_df.loc[:,'tmin'] = (swb_df.loc[:,'tmin'] - 32) / 1.8
swb_df.loc[:,'tmax'] = (swb_df.loc[:,'tmax'] - 32) / 1.8
swb_df.loc[:,'tmean'] = (swb_df.loc[:,'tmean'] - 32) / 1.8
swb_df.loc[:,'gross_precip'] = swb_df.loc[:,'gross_precip'] * 25.4
swb_df.loc[:,'actual_ET'] = swb_df.loc[:,'actual_ET'] * 25.4
swb_df.loc[:,'reference_ET0'] = swb_df.loc[:,'reference_ET0'] * 25.4
swb_df.loc[:,'soil_storage'] = swb_df.loc[:,'soil_storage'] * 25.4
swb_df.loc[:,'snow_storage'] = swb_df.loc[:,'snow_storage'] * 25.4
swb_df.loc[:,'snowfall'] = swb_df.loc[:,'snowfall'] * 25.4
swb_df.loc[:,'snowmelt'] = swb_df.loc[:,'snowmelt'] * 25.4
swb_df.loc[:,'net_infiltration'] = swb_df.loc[:,'net_infiltration'] * 25.4
swb_df.loc[:,'infiltration'] = swb_df.loc[:,'infiltration'] * 25.4

swb_df['date'] = pd.to_datetime(swb_df['date'])

# swb2 still uses Imperial units (inches and feet); the Python code expects metric units (mm and m).
# The example control file we're using for swb2 specifies 3.6 inches/foot for the available water capacity.
# 3.6 inches per foot equals 300 mm/m. The rooting depth is specified in the swb2 lookup table as 1.6404 feet, 
# or 1.6404 ft / 3.2808 ft/m = 0.5 m
#mycell = SWBCell(latitude=60.57154, available_water_capacity=300., rooting_depth=0.5, calculation_method='tm_exp')


mycell_tm = SWBCell(latitude=60.57154, available_water_capacity=300., rooting_depth=1.0, calculation_method='tm_table',
                    thornthwaite_mather_df=tm_soil_moisture_retention_df)

#mycell.init_swb_cell()
mycell_tm.init_swb_cell()

#for index, row in swb_df.iterrows():
#    mycell.calc_cell_water_budget(int(row['year']),int(row['month']),int(row['day']),
#                                  row['tmin'],row['tmax'],row['tmean'],row['gross_precip'])
#    mycell.variables_todict()

for index, row in swb_df.iterrows():
    mycell_tm.calc_cell_water_budget(int(row['year']),int(row['month']),int(row['day']),
                                     row['tmin'],row['tmax'],row['tmean'],row['gross_precip'])
    mycell_tm.variables_todict()

mycell_tm.convert_dict_to_df()
py_tm_df = mycell_tm.output_df.copy()
py_tm_df.loc[:,'date'] = pd.to_datetime(py_tm_df['date'])