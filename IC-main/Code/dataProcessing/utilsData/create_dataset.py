import pandas as pd
import numpy as np
import os
from data_processing import DataProcessing

files = os.listdir('../../dataset/prices_data')
for file in files:
    data_processed = DataProcessing(pd.read_csv(f'../../dataset/prices_data/{file}'))
    data_processed.create_return_by_period(name_return='Daily_Return', period=1, remove_nan=False)
    data_processed.create_return_by_period(name_return='Week_Return', period=6, remove_nan=False)
    data_processed.create_return_by_period(name_return='Month_Return', period=22, remove_nan=False)
    data_processed.create_cumulative_std(name_return='Daily_Return')
    data_processed.create_cumulative_std(name_return='Week_Return')
    data_processed.create_cumulative_std(name_return='Month_Return')
    data_processed.create_indicator(name_return='Daily_Return', factor=0.1)
    data_processed.create_indicator(name_return='Week_Return', factor=0.1)
    data_processed.create_indicator(name_return='Month_Return', factor=0.1)
    data_processed.dataframe.to_csv(f'../../dataset/prices_processed/{file}', index_label=False)
    print(f'File {file} created and save in ../dataset/prices_processed/{file}')



