
import dicom2nifti
import os
from matplotlib import pyplot as plt
import imageio.v2 as iio2
import nibabel as nib
import scipy.ndimage as ndi
import numpy as np
import torchio


class Process():

    def __init__(self):

        self.source = './AD01_MR_DICOM/'
        self.niftiPath = './nifti/'

    def displayOne(self, imgFileName, axial=52, from_file=True, ext='nii'):
        """
        plotting function
        takes any picture file to read from local folders, nifti images as files, nibabel image object or 3D array  

        args:
        imgFileName : string, img or array object
        axial : int axial slice to be displayed from the 3D image
        from_file : boolean
        ext : string
        """

        if from_file and imgFileName.endswith('.nii'):
            imgWithHeader = nib.load(self.niftiPath+imgFileName)
            img=imgWithHeader.dataobj
            #print(imgWithHeader.header) # access metadata
            plt.imshow(ndi.rotate(img[:,axial,:],90))

        elif not from_file and ext=='nii':
            if not isinstance(imgFileName, np.ndarray):
                img=imgFileName.dataobj
            else:    
                img = imgFileName
            plt.imshow(ndi.rotate(img[:,axial,:],90))

        else:
            img = iio2.imread(self.source+imgFileName)
            #print(img.meta) # access metadata
            plt.imshow(img)
        plt.show()

    def convertToNifti(self, singleSeries=True):
        """
        convert DICOM to NIfTI
        saves the nifti image composed from a single series stacked DICOM files
        meta data is preserved
        """

        if not os.path.exists(self.niftiPath):
            os.mkdir(self.niftiPath)
        if singleSeries:
            FirstFileName=os.listdir(self.source)[0]
            dicomSeries_to_NiftiFileName='_'.join(FirstFileName.split('_')[:-1])
            dicom2nifti.dicom_series_to_nifti(self.source, os.path.join(self.niftiPath,dicomSeries_to_NiftiFileName), reorient_nifti=True)

    def getNifti(self, imgFileName):
        """
        loads in memory a local nifti file

        args:
        imgFileName : string
        """

        self.niftiImgWithHeader = nib.load(self.niftiPath+imgFileName)
        # Use img=imgWithHeader.get_fdata() to get a Numpy memmap instead of a Numpy ndarray
        self.niftiImg = np.asarray(self.niftiImgWithHeader.dataobj)
    
    def NiftiTransform(self, samplingTuple=None, sizeTuple=None):
        """
        applies resampling based on a pixel spacing distance input or target image size

        args:
        samplingTuple : tuple(float,float,float) or None
        sizeTuple : tuple(int,int,int) or None
        both argugments must be passed, one of them being None
        """

        if sizeTuple is None:
            transform=torchio.Resample(samplingTuple)
            self.niftiImg=transform(np.expand_dims(self.niftiImg,0)).squeeze()
        if samplingTuple is None:
            transform=torchio.Resize(sizeTuple)
            self.niftiImg=transform(np.expand_dims(self.niftiImg,0)).squeeze()
    
    def Filter(self, minmax=(-1,1)):
        """
        applies image pixel intensity scaling

        args:
        minmax : tuple(min_value,max_value)
        """

        transform=torchio.RescaleIntensity(out_min_max=minmax)
        self.niftiImg=transform(np.expand_dims(self.niftiImg,0)).squeeze()



if __name__ == "__main__":

    set=Process()
    set.convertToNifti()
    set.displayOne('anon_AD01.nii',axial=52)
    set.getNifti('anon_AD01.nii')
    set.NiftiTransform(samplingTuple=(0.5,0.5,0.5),sizeTuple=None)
    set.Filter()
    set.displayOne(set.niftiImg, axial=104, from_file=False)