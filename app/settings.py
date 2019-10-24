# -*- coding: utf-8 -*-

import sys
from pathlib import Path

class Settings:
  APP_ROOT_PATH = str(Path(sys.argv[0]).resolve().parent)
  # files and directories
  CONFIG_FILE_PATH = r'.\settings.ini'
  LOG_FILE_NAME = 'diff.log'
  SNAPSHOT_LIST_FILE_NAME = 'list.csv'
  TEMP_FILE_NAME = 'temp.txt'
  FAILBACK_FILE_NAME = 'failback.txt'

  # Snapshot
  MAX_SNAPSHOT_INDEX = 15



