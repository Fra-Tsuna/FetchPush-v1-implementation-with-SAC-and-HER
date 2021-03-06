#!/usr/bin/env python3

import numpy as np
import tensorflow as tf


NORMALIZATION = "Gaussian"

"""
Based on https://github.com/TianhongDai/hindsight-experience-replay/blob/master/mpi_utils/normalizer.py
"""


class Normalizer:
    
    def __init__(self, size, eps=1e-2, clip_range=np.inf, 
                 normalization=NORMALIZATION):
        self.size = size
        self.eps = eps
        self.clip_range = clip_range
        self.normalization = normalization

        if self.normalization == "Gaussian":
            self.local_sum = np.zeros(self.size, np.float32)
            self.local_sumsq = np.zeros(self.size, np.float32)
            self.local_count = np.zeros(1, np.float32)
            self.mean = np.zeros(self.size, np.float32)
            self.std = np.ones(self.size, np.float32)
        elif self.normalization == "MinMax":
            self.min = np.zeros(self.size, np.float32)
            self.max = np.ones(self.size, np.float32)
        else:
            raise TypeError("Wrong normalization type")

    def update(self, buffer):
        if self.normalization == "Gaussian":
            self.local_sum += buffer.sum(axis=0)
            self.local_sumsq += (np.square(buffer)).sum(axis=0)
            self.local_count[0] += buffer.shape[0]
            self.mean = self.local_sum / self.local_count
            self.std = np.sqrt(np.maximum(np.square(self.eps), 
                                          (self.local_sumsq / self.local_count) - 
                                           np.square(self.local_sum / self.local_count)))
        elif self.normalization == "MinMax":
            self.min = np.minimum(self.min, buffer.min(axis=0))
            self.max = np.maximum(self.max, buffer.max(axis=0))
        
    def normalize(self, vector, clip_range=None):
        if clip_range is None:
            clip_range = self.clip_range
        if self.normalization == "Gaussian":
            v_norm = (vector - self.mean) / self.std
        elif self.normalization == "MinMax":
            v_norm = (vector - self.min) / (self.max - self.min)
        return np.clip(v_norm, -clip_range, clip_range)
