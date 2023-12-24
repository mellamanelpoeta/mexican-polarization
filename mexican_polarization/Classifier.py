# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_classifier.ipynb.

# %% auto 0
__all__ = ['Classifier']

# %% ../nbs/02_classifier.ipynb 3
import pandas as pd
import numpy as np

# %% ../nbs/02_classifier.ipynb 9
class Classifier:

    def load_embeddings(file_path):
        '''Loads the embeddings from a file and returns a dictionary with the words as keys and the vectors as values'''
        word_to_vec = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                values = line.split()
                word = values[0]
                vector = np.array(values[1:], dtype='float32')
                print(vector.shape)
                word_to_vec[word] = vector
        return word_to_vec
