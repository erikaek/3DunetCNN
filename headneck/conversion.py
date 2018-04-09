import nibabel as nib
import numpy as np
import os.path
import itk
import math
import glob
import nrrd
import SimpleITK as sitk

def downsample(data,factor):
    return data[::factor,::factor,::factor]

def pad_zdim(data,zlim,value):

    new_data = np.multiply(np.ones((data.shape[0],data.shape[1],zlim),dtype=data.dtype),value)

    i_start = int(math.floor((zlim-data.shape[2])/2))
    iz_old = 0
    for iz_new in range(i_start,i_start+data.shape[2]):
        new_data[:,:,iz_new] = data[:,:,iz_old]
        iz_old+=1

    return new_data

def create_affine(nrrdheader,downsample_factor):

    affine = np.eye(4)
    origin = nrrdheader['space origin']

    for i in range(len(origin)):
        affine[i,3] = float(origin[i])/downsample_factor

    return affine


def alter_header(nrrdheader,img):
    
    space_dir = nrrdheader['space directions']
    img.header['pixdim'][1:4] = [space_dir[0][0], space_dir[1][1], space_dir[2][2]]

    return img

for readpath in glob.glob(os.path.join("../../Data", "*","*")):

    subject = os.path.basename(readpath)

    savepath = os.path.join('data/original/', os.path.basename(os.path.dirname(readpath)),
                                              subject)
    organfile = os.path.join(readpath,"structures","Mandible.nrrd")

    if os.path.exists(organfile):

        if not os.path.exists(savepath):
            os.makedirs(savepath)
   
        ct_data, info_ct = nrrd.read(readpath+'/img.nrrd')
        label_data, info_label = nrrd.read(organfile)

        ct_data = downsample(ct_data,2)
        label_data = downsample(label_data,2)

        ct_data = pad_zdim(ct_data,180,0)
        label_data = pad_zdim(label_data,180,0)

        affine = create_affine(info_ct,2)

        ct_img = nib.Nifti1Image(ct_data, affine)
        label_img = nib.Nifti1Image(label_data, affine)

        ct_img = alter_header(info_ct,ct_img)
        label_img = alter_header(info_ct,label_img)

        nib.save(ct_img, savepath+'/ct.nii.gz')
        nib.save(label_img, savepath + '/truth.nii.gz')

