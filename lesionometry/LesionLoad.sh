#!/bin/bash
output_dir="/cubric/data/sapmc3/MS/Lesionmetry/LesionLoad"
working_dir="/cubric/data/sapmc3/Emma/processed"
tract_dir="/cubric/scratch/sapmc3/Emma/reprocessed"

for sub in "s1" "s2" "s3" "s4" "s5" "s6" "s7" "s8" "s9" "s10" "s11" "s12" "s13" "s14" "s15" "s16" "s17" "s18" "s19" "s20" \
"s21" "s22" "s23" "s24" "s25" "s26" "s27" "s28" "s29" "s30" "s31" "s32" "s33" "s34" "s35" "s36" "s37" "s38" "s39" "s40"

do
    lesions=$working_dir/$sub/lesions2b0.nii.gz
    brain=$working_dir/$sub/FLAIR2b0.nii.gz
    tracts=$tract_dir/$sub/Tracts2/TOM_trackings
    # Lesion load
    ##############
    #fslmaths $brain -bin $working_dir/$sub/bin.nii.gz 
    #fslmaths $working_dir/$sub/bin.nii.gz -roi 0 127 0 -1 0 -1 0 -1 $working_dir/$sub/halfbin.nii.gz
    #scil_flip_volume_locally.py $working_dir/$sub/halfbin.nii.gz $working_dir/$sub/halfbin_flip.nii.gz -x -f 
    #mrcalc $working_dir/$sub/halfbin_flip.nii.gz $lesions -mult $working_dir/$sub/halfles_flip.nii.gz
    compute_LL.py $working_dir/$sub/halfles_flip.nii.gz $working_dir/$sub/halfbin_flip.nii.gz -o $output_dir/left_lesionvol -s $sub
    
    # Tractogram load
    ##################
    #mkdir $output_dir/$sub
    #combine all tseg
    #tckedit $tracts/*.tck $output_dir/$sub/combined_tracts.tck -force
    #tckedit with lesions
    #tckedit $output_dir/$sub/combined_tracts.tck -include $lesions $output_dir/$sub/lesioned_tracts.tck -force
    #tckmap
    #tckmap $output_dir/$sub/combined_tracts.tck $output_dir/$sub/combined_tracts.nii.gz -template $lesions -force
    #tckmap $output_dir/$sub/lesioned_tracts.tck $output_dir/$sub/lesioned_tracts.nii.gz -template $lesions -force
    #LL
    #compute_LL.py $output_dir/$sub/lesioned_tracts.nii.gz $output_dir/$sub/combined_tracts.nii.gz -o $output_dir/TractLoad -s $sub
    
done
