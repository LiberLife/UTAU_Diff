# -*- coding: utf-8 -*-

from pathlib import Path
import csv
import shutil
import subprocess
from settings import Settings
from utility import Utility


class Snapshot:
  __config = None
  __snapshot_dir_path = None
  __snapshot_list_file_path = None
  __data_file_path = None
  __list_rows = []

  def __init__(self, config, data_file_path):
    self.__config = config
    self.__snapshot_dir_path = Utility.build_path(
        config['common']['snapshots_dir'])
    self.__snapshot_list_file_path = Path(
        self.__snapshot_dir_path.joinpath(Settings.SNAPSHOT_LIST_FILE_NAME))
    self.__data_file_path = data_file_path
    if self.__snapshot_dir_path.exists() == False:
      self.__snapshot_dir_path.mkdir()
    self.__read_snapshot_list()


  @property
  def list_rows(self):
    return self.__list_rows


  def save_snapshot(self, index, name, message):
    snapshot_file_path = self.build_snapshot_file_path(index)
    if snapshot_file_path.exists():
      snapshot_file_path.unlink()
    shutil.copy(str(self.__data_file_path), str(snapshot_file_path))
    # list
    self.__write_snapshot_list(index, name, message)


  def show_diff(self, index):
    win_merge_file_path = Utility.build_path(
        self.__config['app']['win_merge_file'])
    snapshot_file_path = self.build_snapshot_file_path(index)
    subprocess.call([str(win_merge_file_path), str(
        snapshot_file_path), str(self.__data_file_path)])


  def remove_a_snapshot(self, index):
    snapshot_file_path = self.build_snapshot_file_path(index)
    if snapshot_file_path.exists():
      snapshot_file_path.unlink()
    # list
    with open(str(self.__snapshot_list_file_path), 'w', newline='') as file_handler:
      writer = csv.writer(file_handler)
      for row in self.__list_rows:
        if row['index'] != str(index):
          writer.writerow(row.values())


  def remove_all_snapshot(self):
    for row in self.__list_rows:
      index = row['index']
      snapshot_file_path = self.build_snapshot_file_path(index)
      if snapshot_file_path.exists():
        snapshot_file_path.unlink()
    # list
    self.__snapshot_list_file_path.unlink()


  def build_snapshot_file_path(self, index):
    return self.__snapshot_dir_path.joinpath(str(index).zfill(2) + '.txt')


  def __read_snapshot_list(self):
    dict_reader = None
    if self.__snapshot_list_file_path.exists():
      with open(str(self.__snapshot_list_file_path), 'r', newline='') as file_handler:
        dict_reader = csv.DictReader(
            file_handler, fieldnames=['index', 'datetime', 'name', 'message'])
        for row in dict_reader:
          self.__list_rows.append(row)


  def __write_snapshot_list(self, index, name, message):
    snapshot_item = [str(index), Utility.dip_timestamp(), name, message]
    with open(str(self.__snapshot_list_file_path), 'w', newline='') as file_handler:
      writer = csv.writer(file_handler)
      if self.__list_rows == []:
        writer.writerow(snapshot_item)
      else:
        snapshot_exists = False
        for row in self.__list_rows:
          if row['index'] != str(index):
            writer.writerow(row.values())
            snapshot_exists = True
        if snapshot_exists != False:
          writer.writerow(snapshot_item)

