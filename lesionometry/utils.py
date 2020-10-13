import numpy as np
import pandas as pd
import os

def calculate_load(numerator, denumerator):
    """
    Calculates the ratio a/b

    Parameters
    ----------
    numerator : float
        The lesioned portion
        
    denumerator : float
        The entire brain or bundle of interest

    Returns
    -------
    load : float 
        The calculated lesion load ratio (as a percentage)

    Examples
    --------
    >>> calculate_load(5,500)
    1.0
    """
    load = np.round(numerator/denumerator * 100, 3)
    return load

def save_load(output_dir, subj, load, col_name):
    dict = {'Subject': subj, col_name: load} 
    df = pd.DataFrame(dict)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(output_dir)
    df.to_csv(output_dir + '/' + col_name + '.csv',index=False, header=False, mode='a')
    