import pandas as pd
import numpy as np
from math import *
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/raphael.poux/Mig verre/Interglad_post_traitement.csv")

def Vickers():
    df = df.loc[df["Vickers Hardness (Typical) ( MPa )"] != 0]
    print(len(df))
    hist = df.hist(column="Vickers Hardness (Typical) ( MPa )", bins = 30)
    plt.show()

def Young():
    df = df.loc[df["Young's Modulus at RT ( GPa )"] != 0]
    print(len(df))
    hist = df.hist(column="Young's Modulus at RT ( GPa )", bins = 30)
    plt.show()

def tenacite():
    df = df.loc[df["Fracture Toughness ( MPa.m1/2 )"] != 0]
    print(len(df))
    hist = df.hist(column="Fracture Toughness ( MPa.m1/2 )", bins = 30)
    plt.show()

def densite():
    df = df.loc[df["Density at RT ( g/cm3 )"] != 0]
    print(len(df))
    hist = df.hist(column="Density at RT ( g/cm3 )", bins = 30)
    plt.show()
