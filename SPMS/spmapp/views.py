import numpy as np
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .queries import *
from spmapp.models import *

# Create your views here.

# list
