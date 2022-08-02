import pandas as pd
import numpy as np


def segments_drain_fuel(series, start_vec, end_vec, type_of_data, window=1):
    drain = pd.DataFrame(index=series.index)
    drain['BEVALUE'] = np.nan
    refueling = pd.DataFrame(index=series.index)
    refueling['BEVALUE'] = np.nan

    for i in range(start_vec.shape[0] - start_vec[start_vec > series.index[0]].shape[0],
                       end_vec[end_vec < series.index[-1]].shape[0]):
        start_ind = np.where(series.index.values == start_vec[i])[0][0]
        end_ind = np.where(series.index.values == end_vec[i])[0][0]
        if type_of_data[i] == 0:
            drain.iloc[start_ind + window - 1:end_ind + window, :] = series.iloc[
                                                                     start_ind + window - 1:end_ind + window]
        else:
            refueling.iloc[start_ind + window - 1:end_ind + window] = series.iloc[
                                                                      start_ind + window - 1:end_ind + window]

    return drain, refueling

def detect_segment(low_value, upp_value, series):
    out_segment = low_value.copy()
    low_arr = low_value[low_value.notna().BEVALUE].index
    upp_arr = upp_value[upp_value.notna().BEVALUE].index
    for i in range(low_arr.shape[0] - 1):
        extreme_point = upp_arr[(upp_arr > low_arr[i]) & (upp_arr < low_arr[i+1])][-1]
        out_segment.loc[low_arr[i]:extreme_point] = series.loc[low_arr[i]:extreme_point]
    extreme_point = upp_arr[(upp_arr > low_arr[-1])][-1]
    if not extreme_point:
        out_segment.loc[series.index>low_arr[-1]] = series.loc[series.index>low_arr[-1]]
    else:
        out_segment.loc[low_arr[-1]:extreme_point] = series.loc[low_arr[-1]:extreme_point]
    return out_segment