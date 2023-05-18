from spmapp.models import *
import django
import pandas as pd

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spms.settings")


django.setup()


vfnames = ["M. Omar", "Tanweer"]

vlnames = ["Rahman", "Hasan"]
