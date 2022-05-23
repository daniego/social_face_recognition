import logging
import sys

ELASTICSEARCH_HOST = "http://127.0.0.1:9200"
ELASTICSEARCH_INDEX = "face_recognition"

DEBUG = False

logging.basicConfig(level=logging.DEBUG)

try:
    from .local_settings import *
except ImportError:
    pass
