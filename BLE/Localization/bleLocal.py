## Localization using BLE Beacons
# ECSE 6964 - Internetworking of Things
# Final Project - Localization

# Using Least Squares for Triangulation
# Mitchell Phillips 661060944
# Chris Ve

# PEP8 Styling 2 spaces per indentation
# Last edited April 12, 2017

# Import Libraries
import math, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint

# Based on the setting the equation which is based on measurements:
# Y = AX