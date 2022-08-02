from dateutil.parser import parse
import pandas as pd
import numpy as np


def convert_to_float(x):
    if type(x)==float:
        return x
    else:
        return float('.'.join(x.split(',')))


def bay_drain(x):
    if x[2] > x[3]:
        return 0
    else:
        return 1


def change_to_date(vec_1):
    return vec_1.apply(lambda x: parse(x))


class PreprocessModels:
    def __init__(self, df1, df2, df3, df4, df5):
        self.df1 = df1
        self.df2 = df2
        self.df3 = df3
        self.df4 = df4
        self.df5 = df5
        self.new_df = df5.merge(df2, on='DTIME').merge(df4, on='DTIME').drop('HEIGHT', axis=1)

    def preprocess_df1(self):
        self.df1['BEVALUE'] = self.df1['BEVALUE'].apply(lambda x: convert_to_float(x))
        self.df1.index = self.df1['DTIME'].apply(lambda x: parse(x))
        self.df1.drop('DTIME', axis=1, inplace=True)
        self.df1.drop(self.df1[self.df1['BEVALUE'] == 0].index, inplace=True)

    def preprocess_df2(self):
        pass

    def preprocess_df3(self):
        self.df3['STARTLEVEL'] = self.df3['STARTLEVEL'].apply(lambda x: convert_to_float(x))
        self.df3['ENDLEVEL'] = self.df3['ENDLEVEL'].apply(lambda x: convert_to_float(x))
        self.df3.drop('TSID', axis=1, inplace=True)
        self.df3['bay/drain'] = self.df3.apply(lambda x: bay_drain(x), axis=1)
        self.df3['STARTDATE'] = change_to_date(self.df3['STARTDATE'])
        self.df3['ENDDATE'] = change_to_date(self.df3['ENDDATE'])

    def preprocess_df4(self):
        pass

    def preprocess_df5(self):
        pass

    def preprocess_new_df(self):
        self.new_df.rename(columns={'BEVALUE_x': 'tachometer', 'BEVALUE_y': 'ingection'}, inplace=True)
        self.new_df['DTIME'] = self.new_df['DTIME'].apply(lambda x: parse(x))
        self.new_df = self.df1.merge(self.new_df, left_index=True,right_on='DTIME')
        self.new_df.index = self.new_df.DTIME.values
        self.new_df.drop(['ingection', 'DTIME'], axis=1, inplace=True)
        
        
    def preprocess_all_df(self):
        self.preprocess_df1()
        self.preprocess_df2()
        self.preprocess_df3()
        self.preprocess_df4()
        self.preprocess_df5()
        self.preprocess_new_df()
