#!/bin/env python3
# -*- encoding: utf-8 -*-

import sys
import os

from libs import *

if __name__ == "__main__":
    # ds_store
    s = ds_store.Scanner("http://www.audit.virzz.com/.DS_Store")
    s.scan()
