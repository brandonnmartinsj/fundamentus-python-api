import pandas as pd
import pandas_gbq
from pandas.io import gbq


df = pd.read_csv('bigquerytable.csv')

my_data = df

my_data.to_gbq(destination_table='teste.api',project_id='quickstart-1581561054221',if_exists='replace')