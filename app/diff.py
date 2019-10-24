# -*- coding: utf-8 -*-

import sys
import configparser
from pathlib import Path
from settings import Settings
from controller.controller import Controller



def read_config(this_dir_path):
  config = None
  config_file_path = Path(this_dir_path).joinpath(Settings.CONFIG_FILE_PATH)
  if Path(config_file_path).is_file():
    config = configparser.ConfigParser()
    config.read(str(config_file_path))
  return config


def main():
  args = sys.argv
  if 1 < len(args) and Path(args[1]).is_file():
    pass
    # Read config file
    config = read_config(Settings.APP_ROOT_PATH)
    # Call Controller
    Controller(Path(args[1]).resolve(), config)



if __name__ == "__main__":
  main()

