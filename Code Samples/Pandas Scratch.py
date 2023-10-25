import matplotlib as plt
import numpy as np
import pandas as pd
df = pd.read_csv("F:\IT Pro\Python Developper\The-Future-Data-Scientist-main\Codes Sample\Branch_3-main\\5000 Sales Records.csv")
# Basics functions and attributes to have an overview about the dataframe.
# print(df.head())
# print(df.tail())
# print(df.info())
# print(df.describe())
# print(df.mean())   # Would requires an entry column passsed as a parameter
# print(df.median()) # Would requires an entry column passsed as a parameter
# print(df.shape)
# ----------Basics functions and attributes to have an overview about the dataframe-------------
# print(df.values)
# print(df.columns)
# print(df.index)
# ---------------------------------Sorting Dataframes------------------------------------------ 
# print(df.sort_values('Region', ascending=False))
# print(df.sort_values(['Region', 'Country'], ascending=[False, True]))
# -------------------------------Subsetting Dataframes------------------------------------------
# print(df['Region'])
# print(df[['Region', 'Country']])
# -------------------------------Subsetting by the method .isin()--------------------------------
# print(df[df['Region'].isin(['Sub-Saharan', 'Middle East and North Africa'])])
# ----------------------------Subsetting based on conditions-------------------------------------
# print(df[(df['Unit Price'] > 300) & (df['Unit Price'] < 400)])

# Aggregating Dataframes

# ------------------------------Some Summary statistics-----------------------------------------
# print(df['Total Profit'].mean())
# print(df['Total Profit'].median())
# print(df['Total Profit'].min())
# print(df['Total Profit'].sum())
# print(df['Total Profit'].max())
# print(df['Total Profit'].mode()) # Return The Mode
# print(df['Total Profit'].var()) # Return The Variance
# print(df['Total Profit'].std()) # Return the Standard Deviation
# print(df['Total Profit'].quantile(0.85)) # Return the Quantile with a percentage from 0.1 to 0.99 
# ------------------------------Aggregating functions with .agg()------------------------------ 
# # It just takes a function to apply on a dataframe, it's usefullness comes from the capability to 
# # use some user-defined functions into the dataframe
# def capper(column) : 
#     return str(column).upper()
# print(df["Country"].agg(capper))
# ------------------------------Cumutative Statistics------------------------------------------ 
# print(df['Total Profit'].cumsum())
# print(df['Total Profit'].cummin())
# print(df['Total Profit'].cummax())
# print(df['Total Profit'].cumprod())
# ----------------------------Dropping Duplicates rows----------------------------------------- 
# print(df.drop_duplicates(subset='Region'))
# -----------------------------Counting Column Values------------------------------------------
# print(df['Region'].value_counts(sort=True))
# print(df['Region'].value_counts(normalize=True))
# -----------------------------Grouping by variables-------------------------------------------
# print(df.groupby(['Region','Item Type'])[['Total Revenue', 'Total Cost']].agg([min, np.mean, np.median, np.std, max]))
# -----------------------------Pivot Tables on 1 varibale--------------------------------------
# print(df.pivot_table(values='Total Revenue', index= 'Country', columns='Total Cost', fill_value = 0, margins = True, aggfunc=[np.min, np.max]))

# ------------------------Slicing and Indexing Dataframes--------------------------------------

# -------------------------------Indexing Dataframes-------------------------------------------
# print(df.set_index(['Region', 'Country'])) #To set a column as an index
# print(df.reset_index(drop=True)) #To drop the column used to be an index with the drop argument set to true it will be removed.
# ---------------------------Subsetting DataFrames with .loc[]---------------------------------
# df_indexed = df.set_index(['Region', 'Country'])
# print(df_indexed.loc[[('Europe', 'Norway') , ('Asia', 'Japan')]]) #Based on levels.
# ----------------------Sorting Dataframe by index with .sort_index[]--------------------------
# df_indexed = df.set_index(['Region', 'Country'])
# print(df_indexed.sort_index(level=['Region', 'Country'] , ascending=[True , False]))
# --------------------Slicing DataFrames with .loc[] and .sort_index[]-------------------------
# df_indexed = (df.set_index(['Region', 'Country'])).sort_index(level=['Region', 'Country'] , ascending=[True , True])
# print(df_indexed.loc['Asia' : 'Europe'])
# print(df_indexed.loc[('Asia', 'Vietnam') : ('Europe', 'Germany')])
# --------------------Slicing DataFrames with .loc[] and .sort_index[]-------------------------
