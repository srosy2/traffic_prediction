import pandas as pd
import numpy as np


def segment_accuracy(predict, ground_truth):
    return float(np.sum(ground_truth.loc[predict.dropna().index].notna().values) / \
                 (np.sum(ground_truth.notna()) + np.sum(ground_truth.loc[predict.dropna().index].isna().values)))
