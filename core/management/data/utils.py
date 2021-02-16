import csv
import pytz
from datetime import datetime


def read_csv_data(path, dtypes=dict()):
  rows = []
  with open(path, newline='') as f:
    reader = csv.DictReader(f, delimiter=',', quotechar='|')
    for row in reader:
      rows.append(row)

    for col, dtype in dtypes.items():
      row[col] = dtype(row[col])

    return rows


def get_utc_datetime(y, m, d):
  return datetime(y, m, d).astimezone(pytz.utc)
