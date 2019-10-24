# -*- coding: utf-8 -*-

import traceback
from controller.dialog import Dialog
from model.logger import Logger
from model.datafile import DataFile
from model.difflist import DiffList
from model.snapshot import Snapshot


class Controller:
  __data_file_path = None
  __config = None
  __data_file = None
  __logger = None

  def __init__(self, data_file_path, config):
    try:
      self.__data_file_path = data_file_path
      self.__config = config
      self.__prepare_logging()
      self.__execute()
    except Exception as e:
      self.__logger.append_error('Exception occurred.', traceback.format_exc())
    finally:
      self.__logger.append_message('Finished.')


  def __prepare_logging(self):
    self.__logger = Logger(self.__config)
    self.__logger.append_data_file_path(self.__data_file_path)


  def __execute(self):
    # data
    self.__data_file = DataFile(self.__data_file_path, self.__config)
    data = self.__data_file.read_data()
    # snapshot
    snapshot = Snapshot(self.__config, self.__data_file_path)
    list_rows = snapshot.list_rows
    # diffs
    diff_list = DiffList(data, self.__config, list_rows)
    diffs = diff_list.create_diffs()
    # dialog
    dialog = Dialog(self.__config, diffs)
    to_do_index = dialog.to_begin_with()
    if to_do_index == Dialog.TO_DO_INDEX_SNAP_DATA:
      file_index, name, message = dialog.snap_data()
      snapshot.save_snapshot(file_index, name, message)
    elif to_do_index == Dialog.TO_DO_INDEX_SHOW_DIFF:
      file_index = dialog.show_diff()
      snapshot.show_diff(file_index)
    elif to_do_index == Dialog.TO_DO_INDEX_REMOVE_A_SNAPSHOT:
      file_index = dialog.remove_a_snapshot()
      snapshot.remove_a_snapshot(file_index)
    elif to_do_index == Dialog.TO_DO_INDEX_REMOVE_ALL_SNAPSHOTS:
      if dialog.remove_all_snapshot():
        snapshot.remove_all_snapshot()
    elif to_do_index == Dialog.TO_DO_INDEX_FAILBACK:
      file_index = dialog.failback()
      snapshot_file_path = snapshot.build_snapshot_file_path(file_index)
      snapshot_data_file = DataFile(snapshot_file_path, self.__config)
      snapshot_data = snapshot_data_file.read_data()
      self.__data_file.rewrite_data(data, snapshot_data)




