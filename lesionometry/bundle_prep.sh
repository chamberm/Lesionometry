#!/bin/bash
output_dir="/cubric/data/sapmc3/MS/Lesionmetry/Subjects"
working_dir="/cubric/scratch/sapmc3/Emma/reprocessed"
data_dir="/cubric/data/sapmc3/Emma/SubDiv"

for sub in "s1" "s2" "s3" "s4" "s5" "s6" "s7" "s8" "s9" "s10" "s11" "s12" "s13" "s14" "s15" "s16" "s17" "s18" "s19" "s20" \
"s21" "s22" "s23" "s24" "s25" "s26" "s27" "s28" "s29" "s30" "s31" "s32" "s33" "s34" "s35" "s36" "s37" "s38" "s39" "s40"

do

    # FETCH METRICS
    mkdir $output_dir/$sub
    mkdir $output_dir/$sub/metrics
    
    cp $data_dir/$sub/metrics/AFD.nii.gz $output_dir/$sub/metrics/
    cp $data_dir/$sub/metrics/FA.nii.gz $output_dir/$sub/metrics/
    cp $data_dir/$sub/metrics/MD.nii.gz $output_dir/$sub/metrics/
    cp $data_dir/$sub/metrics/RD.nii.gz $output_dir/$sub/metrics/
    cp $data_dir/$sub/metrics/RISH2_1200.nii.gz $output_dir/$sub/metrics/
    cp $data_dir/$sub/metrics/RISH2_2400.nii.gz $output_dir/$sub/metrics/
    
    lesions=$data_dir/../processed/$sub/lesions2b0.nii.gz
    
    # FETCH BUNDLES
    mkdir $output_dir/$sub/lesioned
    mkdir $output_dir/$sub/lesioned/trk
    mkdir $output_dir/$sub/bundles
    BUNDLES=$output_dir/$sub/bundles
    TRACTS=${working_dir}/${sub}/Tracts2/TOM_trackings
    LESIONED=$output_dir/$sub/lesioned
    
    cd ${TRACTS}
    for t in "ST_POSTC_right" "ST_PREM_left" "ST_PREM_right" "ST_PREC_left" "ST_PREC_right" "ST_POSTC_left" "AF_left" "AF_right" "UF_left" "UF_right" \
    "CST_left" "CST_right" "ST_FO_left" "ST_FO_right" "ST_PREF_left" "ST_PREF_right" "ST_PAR_left" "ST_PAR_right" "IFO_left" "IFO_right" "CG_left" "CG_right" \
    "ATR_left" "ATR_right" "ILF_left" "ILF_right" "OR_left" "OR_right" "SLF_I_left" "SLF_II_left" "SLF_III_left" "SLF_I_right" \
    "SLF_II_right" "SLF_III_right" "CC_1" "CC_2" "CC_3" "CC_4" "CC_5" "CC_6" "CC_7" "CA"
    do
        tckedit ${TRACTS}/${t}.tck -include $lesions $LESIONED/${t}.tck -force 
        #tck to trk
        size=$(tckinfo ${LESIONED}/${t}.tck | awk 'FNR == 3 { print $2 }')
        if (( $size > 15 )) 
        then
            echo $t
            echo ${filename%.tck}
            #Convert to trk
            scil_convert_tractogram.py ${LESIONED}/${t}.tck ${LESIONED}/trk/${t}.trk \
            --reference ${working_dir}/${sub}/Tracts2/*mask.nii.gz -f
        fi
    done
        
    #Fibers that have a Up down distinction
    for z in "ST_POSTC_right" "ST_PREM_left" "ST_PREM_right" "ST_PREC_left" "ST_PREC_right" "ST_POSTC_left" "AF_left" "AF_right" "UF_left" "UF_right" \
    "CST_left" "CST_right"
    do
        scil_uniformize_streamlines_endpoints.py ${LESIONED}/trk/$z.trk ${BUNDLES}/$z.trk --axis z -f
    done

    #Fibers that have a front and back distinction
    for y in "ST_FO_left" "ST_FO_right" "ST_PREF_left" "ST_PREF_right" "ST_PAR_left" "ST_PAR_right" "IFO_left" "IFO_right" "CG_left" "CG_right" \
    "ATR_left" "ATR_right" "ILF_left" "ILF_right" "OR_left" "OR_right" "SLF_I_left" "SLF_II_left" "SLF_III_left" "SLF_I_right" \
    "SLF_II_right" "SLF_III_right"
    do
        scil_uniformize_streamlines_endpoints.py ${LESIONED}/trk/$y.trk ${BUNDLES}/$y.trk --axis y -f
    done
       
    #Fibers that have a L-R distinction 
    for x in "CC_1" "CC_2" "CC_3" "CC_4" "CC_5" "CC_6" "CC_7" "CA"
    do
        scil_uniformize_streamlines_endpoints.py ${LESIONED}/trk/$x.trk ${BUNDLES}/$x.trk --axis x -f
    done
    

done
  
