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
from lesionometry.utils import calculate_load, save_load

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
                   help='Output directory', required='True')
    
    return p

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
    LL = calculate_load(LesionNo, BrainNo)
    
    #Export to .csv
    subj = [args.subject]
    load = [LL]
    output_dir = args.savename
    save_load(output_dir, subj, load, 'LesionLoad')
    
if __name__ == "__main__":
    main()
