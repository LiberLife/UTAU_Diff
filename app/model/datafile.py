# -*- coding: utf-8 -*-

import configparser
import shutil
import re
from pathlib import Path
from settings import Settings
from utility import Utility


class DataFile:
  __data_file_path = None
  __config = None

  def __init__(self, data_file_path, config):
    self.__data_file_path = data_file_path
    self.__config = config


  def read_data(self):
    data_config = configparser.ConfigParser(allow_no_value=True)
    data_config.optionxform = str
    data_config.read(self.__data_file_path, 'shift-jis')
    return data_config


  def write_data(self, data_config):
    with self.__data_file_path.open(mode='w', encoding='shift-jis') as file_handler:
      data_config.write(file_handler, space_around_delimiters=False)
    self.__copy_data_file(Settings.TEMP_FILE_NAME)


  def rewrite_data(self, data_config, snapshot_data_config):
    with self.__data_file_path.open(mode='w', encoding='shift-jis') as file_handler:
      file_handler.write('')
    has_deleted = False
    with self.__data_file_path.open(mode='a', encoding='shift-jis') as file_handler:
      for section_key in snapshot_data_config.sections():
        # Section key
        if re.match('^\#[0-9]+$', section_key):
          if has_deleted == False:
            self.__delete_old_note_sections(data_config, file_handler)
            has_deleted = True
          file_handler.write('[{0}]\n'.format('#INSERT'))
        else:
          file_handler.write('[{0}]\n'.format(section_key))
        # Params for each section
        for key in snapshot_data_config[section_key].keys():
          if snapshot_data_config[section_key].get(key, raw=True) is None:
            file_handler.write('{0}\n'.format(key))
          else:
            file_handler.write('{0}={1}\n'.format(
                key, snapshot_data_config[section_key].get(key, raw=True)))
    self.__copy_data_file(Settings.FAILBACK_FILE_NAME)



  def __delete_old_note_sections(self, data_config, file_handler):
    for section_key in data_config.sections():
      if re.match('^\#[0-9]+$', section_key):
        file_handler.write('[{0}]\n'.format('#DELETE'))


  def __copy_data_file(self, file_name):
    logs_dir_path = Utility.build_path(self.__config['common']['logs_dir'])
    shutil.copy(str(self.__data_file_path), str(
        logs_dir_path.joinpath(file_name)))


