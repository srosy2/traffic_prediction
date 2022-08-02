from sklearn.metrics import mean_absolute_error
import numpy as np
import pandas as pd
from smoothing import double_exponential_smoothing


def segments(series, scale, window=1):
    rolling_mean = series.rolling(window=window).mean().dropna()
    mae = mean_absolute_error(series[window - 1:], rolling_mean)
    deviation = np.std(series[window - 1:] - rolling_mean)

    lower_bond = rolling_mean - (mae + scale * deviation)
    upper_bond = rolling_mean + (mae + scale * deviation)
    return lower_bond, upper_bond


def detect_anomalies(series, lower_bond, upper_bond, window=1):
    anomalies = pd.DataFrame(index=series.index, columns=series.columns)
    new_series = series[window - 1:].copy()
    anomalies[new_series < lower_bond] = new_series[new_series < lower_bond]
    anomalies[new_series > upper_bond] = new_series[new_series > upper_bond]
    return anomalies


def upper_anomalies(series, alpha, beta, window, scale):
    vec = double_exponential_smoothing(series, alpha, beta)
    lower_bond, upper_bond = segments(vec, scale, window)
    anomalies = detect_anomalies(vec, lower_bond, upper_bond, window)

    return anomalies


def lower_anomalies(series, alpha, beta, window, scale):
    vec = double_exponential_smoothing(series[::-1], alpha, beta)
    lower_bond, upper_bond = segments(vec, scale, window)
    anomalies = detect_anomalies(vec, lower_bond, upper_bond, window)[::-1]

    return anomalies
