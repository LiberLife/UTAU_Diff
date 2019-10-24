# -*- coding: utf-8 -*-

import re


class Diff:
  __data = None
  __snapshot_data = None

  def __init__(self, data, snapshot_data):
    self.__data = data
    self.__snapshot_data = snapshot_data


  def diff(self):
    # Clynp
    is_equal_count = self.__is_equal_count()
    is_equal_length = False
    is_equal_lyric = False
    is_equal_note_num = False
    is_equal_pre_utterance = False
    if is_equal_count == True:
      is_equal_length = True
      is_equal_lyric = True
      is_equal_note_num = True
      is_equal_pre_utterance = True
      data_note_sections = self.__select_note_sections(self.__data)
      snapshot_data_note_sections = self.__select_note_sections(self.__snapshot_data)
      for i in range(len(data_note_sections)):
        if is_equal_length == True:
          if data_note_sections[i]['Length'] != snapshot_data_note_sections[i]['Length']:
            is_equal_length = False
        if is_equal_lyric == True:
          if data_note_sections[i]['Lyric'] != snapshot_data_note_sections[i]['Lyric']:
            is_equal_lyric = False
        if is_equal_note_num == True:
          if data_note_sections[i]['NoteNum'] != snapshot_data_note_sections[i]['NoteNum']:
            is_equal_note_num = False
        if is_equal_pre_utterance == True:
          if data_note_sections[i].get('PreUtterance') != snapshot_data_note_sections[i].get('PreUtterance'):
            is_equal_pre_utterance = False
        if is_equal_length == False and is_equal_lyric == False and is_equal_note_num == False and is_equal_pre_utterance == False:
          break
    evaluation = ''
    evaluation = self.__evaluate(evaluation, is_equal_count, 'C')
    evaluation = self.__evaluate(evaluation, is_equal_length, 'l')
    evaluation = self.__evaluate(evaluation, is_equal_lyric, 'y')
    evaluation = self.__evaluate(evaluation, is_equal_note_num, 'n')
    evaluation = self.__evaluate(evaluation, is_equal_pre_utterance, 'p')
    return evaluation


  def __evaluate(self, evaluation, is_equal, eval_chr):
    if is_equal == True:
      evaluation += eval_chr
    else:
      evaluation += '-'
    return evaluation


  def __is_equal_count(self):
    is_equal_count = False
    data_notes_length = self.__count_notes_length(self.__data)
    if self.__snapshot_data != None:
      snapshot_data_notes_length = self.__count_notes_length(
          self.__snapshot_data)
      is_equal_count = data_notes_length == snapshot_data_notes_length
    return is_equal_count


  def __count_notes_length(self, data):
    notes_length = -1
    if data != None:
      notes_length = len(self.__select_note_sections(data))
    return notes_length


  def __select_note_sections(self, data):
    note_sections = []
    for section_key in data.sections():
      if re.match('^\#[0-9]+$', section_key):
        note_sections.append(data[section_key])
    return note_sections

