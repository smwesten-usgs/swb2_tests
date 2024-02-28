import pathlib as pl
import shutil
import os

def destroy_model_work_output_and_logfile_dirs(base_dir,
                                               swb_work_dir='swb_work',
                                               output_dir='output',
                                               logfile_dir='logfiles'):

  base_path = pl.Path(base_dir)
  swb_work_path = base_path / swb_work_dir
  logfile_path = swb_work_path / logfile_dir
  output_path = swb_work_path / output_dir 
  shutil.rmtree(output_path, ignore_errors=True)
  shutil.rmtree(logfile_path, ignore_errors=True)
  shutil.rmtree(swb_work_path, ignore_errors=True)


def create_model_work_output_and_logfile_dirs(base_dir,
                            swb_work_dir='swb_work',
                            output_dir='output',
                            logfile_dir='logfiles'):

  base_path = pl.Path(base_dir)
  swb_work_path = base_path / swb_work_dir
  logfile_path = swb_work_path / logfile_dir
  output_path = swb_work_path / output_dir 
  swb_work_path.mkdir(parents=True, exist_ok=True)
  logfile_path.mkdir(parents=True, exist_ok=True)
  output_path.mkdir(parents=True, exist_ok=True)


# this is taken from: 
# https://stackoverflow.com/questions/431684/equivalent-of-shell-cd-command-to-change-the-working-directory/13197763#13197763
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)