# -*- coding: utf-8 -*-

from settings import Settings
from utility import Utility
from model.diff import Diff
from model.datafile import DataFile

class DiffList:
  __data = None
  __config = None
  __list_rows = []
  __snapshot_dir_path = None
  __diffs = []

  def __init__(self, data, config, list_rows):
    self.__data = data
    self.__config = config
    self.__list_rows = list_rows
    self.__snapshot_dir_path = Utility.build_path(
        config['common']['snapshots_dir'])
    self.__create_null_diffs()


  def create_diffs(self):
    if self.__list_rows != []:
      for row in self.__list_rows:
        snapshot_file_path = self.__build_snapshot_file_path(row['index'])
        if snapshot_file_path.exists():
          snapshot_data_file = DataFile(snapshot_file_path, self.__config)
          snapshot_data = snapshot_data_file.read_data()
          diff = Diff(self.__data, snapshot_data)
          evaluation = diff.diff()
          self.__rewrite_diffs(evaluation, row)
    return self.__diffs


  def __rewrite_diffs(self, evaluation, row):
    for diff in self.__diffs:
      if diff['index'] == row['index'].zfill(2):
        diff['evaluation'] = evaluation
        diff['datetime'] = row['datetime']
        diff['name'] = row['name']
        diff['message'] = row['message']
        break


  def __create_null_diffs(self):
    for i in range(Settings.MAX_SNAPSHOT_INDEX + 1):
      diff = Diff(self.__data, None)
      evaluation = diff.diff()
      self.__diffs.append({'index': str(i).zfill(
          2), 'evaluation': evaluation, 'datetime': '', 'name': '', 'message': ''})


  def __build_snapshot_file_path(self, index):
    return self.__snapshot_dir_path.joinpath(str(index).zfill(2) + '.txt')
