#!/usr/bin/env python3
import argparse
import csv
import os
import re
import subprocess
import unicodedata
import tarfile
from glob import glob
from multiprocessing import Pool

import progressbar
import sox

from deepspeech_training.util.downloader import SIMPLE_BAR, maybe_download

ARCHIVE_URL = 'http://mowa.clarin-pl.eu/korpusy/audio.tar.gz'
ARCHIVE_NAME = 'clarinstudio.tar.gz'
ARCHIVE_DIR_NAME = 'clarinstudio'

def _download_and_preprocess_data(target_dir):
    # Making path absolute
    target_dir = os.path.abspath(target_dir)
    # Conditionally download data
    archive_path = maybe_download(ARCHIVE_NAME, target_dir, ARCHIVE_URL)
    # Conditionally extract data
    _maybe_extract(target_dir, ARCHIVE_DIR_NAME, archive_path)
    # Produce CSV files
    _maybe_convert_sets(target_dir, ARCHIVE_DIR_NAME)

def _maybe_extract(data_dir, extracted_data, archive):
    extracted_path = os.path.join(data_dir, extracted_data)
    if not os.path.exists(extracted_path):
        print('No directory "%s" - extracting archive...' % extracted_path)
        if not os.path.isdir(extracted_path):
            os.mkdir(extracted_path)
        with tarfile.open(archive) as tar:
            tar.extractall(extracted_path)
    else:
        print('Found directory "%s" - not extracting it from archive.' % archive)
