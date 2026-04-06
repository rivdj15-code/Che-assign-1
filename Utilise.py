import numpy as np

def calculate_concentration(absorbance, epsilon=0.5, path_length=1):
    return absorbance / (epsilon * path_length)

def generate_unknown(epsilon=0.5, path_length=1):
    true_conc = np.random.uniform(0, 10)
    absorbance = epsilon * true_conc * path_length
    return true_conc, absorbance
