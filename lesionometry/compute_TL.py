#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compute tractogram load as the ratio of lesioned streamlines over whole tractogram.

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
    p.add_argument('tractogram', action='store', metavar='tractogram',
                   help='Whole brain tractogram (.tck file)')
    p.add_argument('-s', action='store', metavar='subject', dest='subject',
                   help='Subject ID', required='True')
    p.add_argument('-o', metavar='savename', dest='savename', type=str,
                   help='Output name', required='True')
    
    return p

def main():
    parser = _build_argparser()
    args = parser.parse_args()
    output_dir = args.savename
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load lesions image
    lesions_path = args.lesions
    img_les = nib.load(lesions_path)
    data_les = img_les.get_fdata()
    
    tracts = args.tractogram
    
    #Intersect streamlines with lesion
    os.system("export PATH=/code/mrtrix3/bin:$PATH")
    input_dir = os.path.dirname(tracts)
    input_file_without_ending = os.path.basename(tracts).split(".")[0]
    os.system("tckedit " + tracts + " -include " + lesions + " " + output_dir+"/"+input_file_without_ending+".tck" + " -force")
    
    #Tckmap whole brain and intersected
    os.system("tckmap " + tractogram + " " + join(input_dir, input_file_without_ending)+".nii.gz " + "-template " + lesions_path + " -force")
    
    
    #Compute load
    img_les_tractogram = nib.load(lesioned_tractogram)
    data_les_tractogram = img_les_tractogram.get_fdata()
    
    img_tractogram = nib.load(tractogram)
    data_tractogram = img_tractogram.get_fdata()
    
    #non zero values
    LesionNo = np.count_nonzero(data_les_tractogram)
    TractogramNo = np.count_nonzero(data_tractogram)
    TL = calculate_load(LesionNo, TractogramNo)
    
    #Save
    filename = args.savename
    subj = [args.subject]
    load = [TL]
    
    save_load(output_dir, subj, load, 'TractogramLoad')

if __name__ == "__main__":
    main()
