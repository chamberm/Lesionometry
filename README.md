![Lesionometry](https://github.com/chamberm/Lesionometry/blob/main/ressources/banner.png)
[![Build Status](https://github.com/chamberm/Lesionometry/workflows/Python%20package/badge.svg)](https://github.com/chamberm/Lesionometry/actions)
# Lesionometry
Simple Tractometry-based metrics for characterizing white matter lesions within fibre pathways. This repository contains the scripts used in [Chamberland et al. 2020](https://academic.oup.com/braincomms/advance-article/doi/10.1093/braincomms/fcab065/6207986). If using, please cite the following paper:
```
Mia Winter, Emma C Tallantyre, Thomas AW Brice, Neil P Robertson, Derek K Jones, Maxime Chamberland, Tract-specific MRI measures explain learning and recall differences in multiple sclerosis, Brain Communications, 2021;, fcab065, https://doi.org/10.1093/braincomms/fcab065
```

# Install
This package requires [Mrtrix 3](http://mrtrix.readthedocs.io/en/latest/installation/linux_install.html).
```
J.-D. Tournier, R. E. Smith, D. Raffelt, R. Tabbara, T. Dhollander, M. Pietsch, D. Christiaens, B. Jeurissen, C.-H. Yeh, and A. Connelly. 
MRtrix3: A fast, flexible and open software framework for medical image processing and visualisation. 
NeuroImage, 202 (2019), pp. 116–37.
```

```
git clone https://github.com/chamberm/Lesionometry

python setup.py install
or
pip install -e .
```

# Usage
### Calculate Lesion Load
```
compute_LL.py lesions.nii.gz brain.nii.gz -s SubjectID -o OutputDirectory
```

### Calculate Tractogram Load
```
compute_TL.py lesions.nii.gz tractogram.tck -s SubjectID -o OutputDirectory
```

### Calculate Bundle Load
```
compute_BL.py lesions.nii.gz bundle.tck -s SubjectID -o OutputDirectory
```

# Author
Maxime Chamberland [Website](https://chamberm.github.io/)