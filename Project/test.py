import tkinter as tk
from tkinter import ttk
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt
import pydst
from matplotlib import style

Dst = pydst.Dst(lang='en')

nan1 = Dst.get_data(table_id = "NAN1", variables={'TRANSAKT': ["*"], 'PRISENHED': ["*"], 'Tid': ["*"]})
nan1["INDHOLD"] = pd.to_numeric(nan1["INDHOLD"], errors="coerce")
nan1.dropna(inplace=True)
print(nan1.groupby("TID")["INDHOLD"].mean().head(10))
