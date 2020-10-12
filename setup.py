from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(name='Lesionometry',
        version='0.0.1',
        description='Tractometry-based metrics for characterizing white matter lesions within fibre pathways',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/chamberm/Lesionometry',
        author='Maxime Chamberland',
        author_email='chamberlandM@cardiff.ac.uk',
        python_requires='>=3.7',
        license='MIT License',
        packages=find_packages(),
        install_requires=[
            'future',
            'numpy',
            'matplotlib',
            'pandas',
            'nibabel'
        ],
        zip_safe=False,
        classifiers=[
            'Intended Audience :: Science/Research',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering'
        ],
    )
