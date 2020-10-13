#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compute bundle load as the ratio of lesioned streamlines over entire bundle.

"""

from __future__ import division, print_function, absolute_import
import os
import argparse
from os.path import join

import numpy as np
import nibabel as nib
import pandas as pd
from lesionometry.utils import calculate_load, save_load

def _build_argparser():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('lesions', action='store', metavar='lesions',
                   help='Binary mask of the lesions.')
    p.add_argument('bundle', action='store', metavar='bundle',
                   help='Fiber bundle (.tck file)')
    p.add_argument('-s', action='store', metavar='subject', dest='subject',
                   help='Subject ID', required='True')
    p.add_argument('-o', metavar='savename', dest='savename', type=str,
                   help='Output directory', required='True')
    
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
    
    tracts = args.bundle
    
    #Intersect streamlines with lesion
    os.system("export PATH=/code/mrtrix3/bin:$PATH")
    input_dir = os.path.dirname(tracts)
    input_file_without_ending = os.path.basename(tracts).split(".")[0]
    
    os.system("tckedit " + tracts + " -include " + lesions_path + " " + output_dir+"/"+input_file_without_ending+"_lesioned.tck" + " -force")
    
    #Tckmap whole brain and intersected
    fiber = join(output_dir, input_file_without_ending)+".nii.gz"
    os.system("tckmap " + tracts + " " + output_dir+"/"+input_file_without_ending+".nii.gz" + " -template " + lesions_path + " -force")
    os.system("tckmap " + output_dir+"/"+input_file_without_ending+"_lesioned.tck" + " " + output_dir+"/"+input_file_without_ending+"_lesioned.nii.gz" 
    + " -template " + lesions_path + " -force")
    
    #Compute load
    img_fiber = nib.load(fiber)
    data_fiber = img_fiber.get_fdata()
    
    img_les_fiber = nib.load(output_dir+"/"+input_file_without_ending+"_lesioned.nii.gz")
    data_les_fiber = img_les_fiber.get_fdata()
    
    #non zero values
    LesionNo = np.count_nonzero(data_les_fiber)
    fiberNo = np.count_nonzero(data_fiber)
    BL = calculate_load(LesionNo, fiberNo)
    
    #Save
    filename = args.savename
    subj = [args.subject]
    load = [BL]
    
    save_load(output_dir, subj, load, 'BundleLoad')

if __name__ == "__main__":
    main()
