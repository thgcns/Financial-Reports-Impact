import pandas as pd
import numpy as np


def catalog_return(row, x, name_return):
    if row[name_return] > x * row[f'Cumulative_std_{name_return}']:
        return 1
    elif row[name_return] < -x * row[f'Cumulative_std_{name_return}']:
        return -1
    else:
        return 0


class DataProcessing:
    def __init__(self, data):
        self.dataframe = data
        self.dataframe['Date'] = pd.to_datetime(self.dataframe['Date'])
        self.dataframe = self.dataframe.sort_values(by='Date')

    def get_by_date_range(self, start_date, end_date):
        mask = ((self.dataframe['Date'] >= start_date) & (self.dataframe['Date'] <= end_date))
        return self.dataframe.loc[mask]

    def get_by_date(self, date):
        return self.dataframe.loc[(self.dataframe['Date'] == date)]

    def create_return_by_period(self, name_return, period, remove_nan=False):
        self.dataframe[f'{name_return}'] = np.log(
            self.dataframe['Close'] / self.dataframe['Close'].shift(period))
        if remove_nan:
            self.dataframe = self.dataframe.dropna()

    def create_cumulative_std(self, name_return):
        self.dataframe[f'Cumulative_std_{name_return}'] = self.dataframe[name_return].expanding().std()

    def create_indicator(self, name_return, factor):
        self.dataframe[f'Indicator_{name_return}'] = self.dataframe.apply(lambda row:
                                                                          catalog_return(row, factor, name_return),
                                                                          axis=1)

