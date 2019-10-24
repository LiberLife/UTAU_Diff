# -*- coding: utf-8 -*-

from pathlib import Path
from settings import Settings
from utility import Utility


class Logger:
  __config = None
  __log_file_path = None

  def __init__(self, config):
    self.__config = config
    logs_dir_path = Utility.build_path(config['common']['logs_dir'])
    self.__log_file_path = Path(logs_dir_path.joinpath(Settings.LOG_FILE_NAME))
    if logs_dir_path.exists() == False:
      logs_dir_path.mkdir()


  def append_data_file_path(self, data_file_path):
    with open(str(self.__log_file_path), mode='a', encoding='utf-8') as f:
      f.write('[{0}] Read file: {1}\n'.format(
          Utility.dip_timestamp(), data_file_path))


  def append_error(self, message, exception):
    with open(str(self.__log_file_path), mode='a', encoding='utf-8') as f:
      f.write('[{0}] Error: {1}\n Exception.message: {2}\n'.format(
          Utility.dip_timestamp(), message, str(exception)))


  def append_message(self, message):
    with open(str(self.__log_file_path), mode='a', encoding='utf-8') as f:
      f.write('[{0}] Message: {1}\n'.format(
          Utility.dip_timestamp(), message))


