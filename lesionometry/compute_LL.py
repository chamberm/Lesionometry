#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compute lesion load as the ratio of lesions over brain mask.

IMPORTANT: All images must have the same dimensions and datatype.
"""

from __future__ import division, print_function, absolute_import
import os
import argparse

import numpy as np
import nibabel as nib
import pandas as pd

def _build_argparser():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('lesions', action='store', metavar='lesions',
                   help='Binary mask of the lesions.')
    p.add_argument('brain', action='store', metavar='brain',
                   help='Brain extracted image (or white matter mask)')
    p.add_argument('-s', action='store', metavar='subject', dest='subject',
                   help='Subject ID', required='True')
    p.add_argument('-o', metavar='savename', dest='savename', type=str,
                   help='Output name', required='True')
    
    return p

def calculate_ratio(numerator, denumerator):
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
    >>> calculate_ratio(5,500)
    1.0
    """
    LL = np.round(numerator/denumerator * 100, 3)
    return LL

def main():
    parser = _build_argparser()
    args = parser.parse_args()

    # Load lesions image
    lesions_path = args.lesions
    img_les = nib.load(lesions_path)
    data_les = img_les.get_fdata()

    # Load brain image
    brain_path = args.brain
    img_brain = nib.load(brain_path)
    data_brain = img_brain.get_fdata()
    
    #non zero values (brain needs to be Betted)
    LesionNo = np.count_nonzero(data_les)
    BrainNo = np.count_nonzero(data_brain)
    
    #Simple lesion load
    LL = calculate_ratio(LesionNo, BrainNo)
    
    #Export to .csv
    filename = args.savename
    subj = [args.subject]
    LesionLoad = [LL]
    dict = {'Subject': subj, 'LesionLoad': LesionLoad}  
    
    df = pd.DataFrame(dict)
    df.to_csv(filename + '.csv',index=False, header=False, mode='a')


if __name__ == "__main__":
    main()
