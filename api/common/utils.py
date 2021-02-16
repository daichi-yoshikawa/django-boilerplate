import datetime
import pytz
import random
import string


ASCII_LETTERS = string.ascii_letters + string.digits
ASCII_LETTERS_LIST = [c for c in ASCII_LETTERS]

def generate_random_letters(length):
  return ''.join(random.choices(ASCII_LETTERS_LIST, k=length))

def get_utc_now():
  return datetime.datetime.utcnow().astimezone(pytz.utc)

def to_utc(date):
  return date.astimezone(pytz.utc)

def get_far_future_datetime():
  return to_utc(datetime.datetime(2999, 12, 31))
