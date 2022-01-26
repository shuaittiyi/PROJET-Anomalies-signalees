from ast import increment_lineno
from tkinter import Variable
import seaborn as sns
import pandas
import csv
import numpy
import numpy as np
import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
print(pandas.__version__)

df = pandas.read_csv(r"C:\projet\python\panda\dans_ma_rue.csv", sep = ';' , header = 0)