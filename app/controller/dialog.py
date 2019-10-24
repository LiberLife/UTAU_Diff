# -*- coding: utf-8 -*-

import re
import random
import string
from settings import Settings
from utility import Utility


class Dialog:
  TO_DO_INDEX_SNAP_DATA = 0
  TO_DO_INDEX_SHOW_DIFF = 1
  TO_DO_INDEX_REMOVE_A_SNAPSHOT = 2
  TO_DO_INDEX_REMOVE_ALL_SNAPSHOTS = 3
  TO_DO_INDEX_FAILBACK = 4

  __config = None
  __diffs = None

  def __init__(self, config, diffs):
    self.__config = config
    self.__diffs = diffs


  def to_begin_with(self):
    print('Use Ctrl-Z plus Return to quit.')
    print('Snapshots:')
    has_snapshot = False
    for diff in self.__diffs:
      print('  ' + ' '.join(diff.values()))
      if has_snapshot == False and diff['name'] != '':
        has_snapshot = True
    print()
    # Select what to do
    to_do_index = Dialog.TO_DO_INDEX_SNAP_DATA
    if has_snapshot == False:
      print('No snapshots now...')
    else:
      print('What do you do?')
      print('  {0}. Snap data'.format(Dialog.TO_DO_INDEX_SNAP_DATA))
      print('  {0}. Show diff'.format(Dialog.TO_DO_INDEX_SHOW_DIFF))
      print('  {0}. Remove a snapshot'.format(
          Dialog.TO_DO_INDEX_REMOVE_A_SNAPSHOT))
      print('  {0}. Remove all snapshots'.format(
          Dialog.TO_DO_INDEX_REMOVE_ALL_SNAPSHOTS))
      print('  {0}. Failback'.format(
          Dialog.TO_DO_INDEX_FAILBACK))
      while True:
        answer = input('Select task(0~4)[0]: ')
        if answer == '':
          answer = 0
        if self.__is_valid(answer, 4, 0):
          to_do_index = int(answer)
          break
    print()
    return to_do_index


  def snap_data(self):
    file_index = 0
    for diff in self.__diffs:
      if diff['name'] == '':
        file_index = int(diff['index'])
        break
    while True:
      answer = input('Snap data! Select index(0~{0})[{1}]: '.format(
          str(Settings.MAX_SNAPSHOT_INDEX), file_index))
      if answer == '':
        answer = file_index
      if self.__is_valid(answer, Settings.MAX_SNAPSHOT_INDEX, 0):
        if self.__snapshot_exists(answer):
          yn = input('Overwrite existing snapshot?(y|n)[y]: ')
          if yn == '':
            yn = 'y'
          if re.match('[^(no|n)]', yn.lower()):
            file_index = int(answer)
            name, message = self.__ask_name_and_message(file_index)
            break
        else:
          file_index = int(answer)
          name, message = self.__ask_name_and_message(file_index)
          break
    return file_index, name, message


  def show_diff(self):
    file_index = 0
    for diff in self.__diffs:
      if diff['name'] != '':
        file_index = int(diff['index'])
        break
    while True:
      answer = input('Show diff! Select index(0~{0})[{1}]: '.format(
          str(Settings.MAX_SNAPSHOT_INDEX), file_index))
      if answer == '':
        answer = file_index
      if self.__is_valid(answer, Settings.MAX_SNAPSHOT_INDEX, 0):
        if self.__snapshot_exists(answer):
          file_index = int(answer)
          break
    return file_index


  def remove_a_snapshot(self):
    file_index = 0
    for diff in self.__diffs:
      if diff['name'] != '':
        file_index = int(diff['index'])
        break
    while True:
      answer = input('Remove a snapshot! Select index(0~{0})[{1}]: '.format(
          str(Settings.MAX_SNAPSHOT_INDEX), file_index))
      if answer == '':
        answer = file_index
      if self.__is_valid(answer, Settings.MAX_SNAPSHOT_INDEX, 0):
        if self.__snapshot_exists(answer):
          file_index = int(answer)
          break
    return file_index


  def remove_all_snapshot(self):
    should_remove = False
    yn = input('Remove all snapshots! Really?(y|n)[y]: ')
    if yn == '':
      yn = 'y'
    if re.match('(yes|y)', yn.lower()):
      should_remove = True
    return should_remove


  def failback(self):
    file_index = 0
    for diff in self.__diffs:
      if diff['name'] != '':
        file_index = int(diff['index'])
        break
    while True:
      answer = input('Failback! Select index(0~{0})[{1}]: '.format(
          str(Settings.MAX_SNAPSHOT_INDEX), file_index))
      if answer == '':
        answer = file_index
      if self.__is_valid(answer, Settings.MAX_SNAPSHOT_INDEX, 0):
        if self.__snapshot_exists(answer):
          file_index = int(answer)
          break
    return file_index


  def __ask_name_and_message(self, file_index):
    random_name = ''.join(random.choices(
        string.ascii_letters + string.digits, k=6))
    name = input('Input snapshot name[{0}]: '.format(random_name))
    if name == '':
      name = random_name
    message = input('Input message: ')
    return name, message


  def __snapshot_exists(self, index):
    snapshot_exists = False
    for diff in self.__diffs:
      if diff['index'] == str(index).zfill(2):
        if diff['name'] != '':
          snapshot_exists = True
        break
    return snapshot_exists


  def __is_valid(self, target, max, min):
    is_valid = False
    if re.match('^\+?([1-9][0-9]*|0)$', str(target)):
      target_number = int(target)
      if min <= target_number and target_number <= max:
        is_valid = True
    return is_valid



