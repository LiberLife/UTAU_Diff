# -*- coding: utf-8 -*-

import datetime
from pathlib import Path
from settings import Settings

class Utility:
  @staticmethod
  def build_path(path):
    resolved_path = path
    if isinstance(resolved_path, str):
      resolved_path = Path(resolved_path)
    if resolved_path.is_absolute() == False:
      resolved_path = Path(Path(Settings.APP_ROOT_PATH).joinpath(resolved_path))
    return resolved_path

  @staticmethod
  def dip_timestamp():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')
