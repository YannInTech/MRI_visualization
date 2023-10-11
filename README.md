# MRI visualization

## Subject

This repository provides imaging processing capabilities for NIfTI 3D data and covers the following functions:  
1. Convert MRI scans from DICOM to NIfTI format  
2. Plot MRI scans  
3. Resampling and resizing  
4. N4 correction of MRI scans  
5. Brain Extraction  

## Files

mri.py  
visual.ipynb  
environment.yml  

## Description

environment.yml contains the python conda environment libraries required for this program  

mri.py implements the Process class and a main method that instantiates it and calls methods in order to convert the DICOM series into one NIfTI file,
loads it, executes a resampling that double the scans resolution, filters and rescales to a given pixel intensities interval and plots the resulting image at the start and end stage.  
Note the second display call loads the axial slice of the MRI image at an index double that of the first display, although the slice is identical. That is to verify the resampling was executed as expected.  

visual.ipynb implements the axial, sagittal and coronal 3D visualization of the MRI image and the brain segment extraction  
