import os
import importlib.resources as pkg_resources

import numeral_converter


NUMERAL_CONVERTER_DATA_PATH = pkg_resources.files(package=numeral_converter) / 'resource'


DEFAULT_TOPN_LEAVES = os.getenv('DEFAULT_TOPN_LEAVES', 10)
MIN_CORRECTION_PRICE = os.getenv('MIN_CORRECTION_PRICE', 1e-5)
MAX_CORRECTION_RATE = os.getenv('MAX_CORRECTION_RATE', 2/3)

DEFAULT_DELETION_PRICE = .4
DEFAULT_SUBSTITUTION_PRICE = .2
DEFAULT_INSERTION_PRICE = .05
DEFAULT_TRANSPOSITION_PRICE = .35
