

import vtk
import nrrd
import os.path

def readnrrd(filename):
    """Read image in nrrd format."""
    reader = vtk.vtkNrrdReader()
    reader.SetFileName(filename)
    reader.Update()
    info = reader.GetInformation()
    return reader.GetOutput(), info

def writenifti(image,filename, info):
    """Write nifti file."""
    writer = vtk.vtkNIFTIImageWriter()
    writer.SetInputData(image)
    writer.SetFileName(filename)
    writer.SetInformation(info)
    writer.Write()

def definefolders():
    organs = ['BrainStem', 'Chiasm', 'Mandible', 'OpticNerve_L', 'OpticNerve_R','Parotid_L',
              'Parotid_R', 'Submandibular_L', 'Submandibular_R'];

    part1_part2_fold = ['0522c0001', '0522c0002', '0522c0003', '0522c0009', '0522c0013',
    '0522c0014', '0522c0017', '0522c0057', '0522c0070', '0522c0077', '0522c0079',
    '0522c0081', '0522c0125', '0522c0132', '0522c0147', '0522c0149', '0522c0159',
    '0522c0161', '0522c0190', '0522c0195', '0522c0226', '0522c0248', '0522c0251',
    '0522c0253', '0522c0328','0522c0329', '0522c0330', '0522c0427', '0522c0433', '0522c0441',
    '0522c0455', '0522c0457', '0522c0479'];

    part3_fold = ['0522c0555', '0522c0576', '0522c0598', '0522c0659', '0522c0661',
    '0522c0667', '0522c0669', '0522c0708', '0522c0727', '0522c0746'];

    part4_fold = ['0522c0788', '0522c0806', '0522c0845', '0522c0857', '0522c0878'];

    part_folders = ['PDDCA-1.4.1_part1_part2', 'PDDCA-1.4.1_part3', 'PDDCA-1.4.1_part4']

    data_folders = {0 : part1_part2_fold, 1 : part3_fold, 2 : part4_fold};

    return organs, part_folders, data_folders

organs, part_folders, data_folders = definefolders()

for i_pf in range(2):

    pf = part_folders[i_pf]

    for df in data_folders[i_pf]:
        readpath = '../../Data/'+pf+'/'+df+'/'
        savepath = 'data/original/'+df+'/'

        if not os.path.exists(savepath):
            os.makedirs(savepath)

        if os.path.exists(readpath+'structures/'+organs[2]+'.nrrd'):
            label_data, info = nrrd.read(readpath+'structures/'+organs[2]+'.nrrd')
            writenifti(label_data, savepath + 'labels.nii.gz', info)
            ct_data, info = nrrd.read(readpath+'img.nrrd')
            writenifti(ct_data, savepath+'img.nii.gz', info)




"""for i_pf in range(2):

    pf = part_folders[i_pf]

    for df in data_folders[i_pf]:
        readpath = '../../Data/'+pf+'/'+df+'/'
        savepath = 'data/original/'+df+'/'

        if not os.path.exists(savepath):
            os.makedirs(savepath)

        if os.path.exists(readpath+'structures/'+organs[2]+'.nrrd'):
            label_data, info = readnrrd(readpath+'structures/'+organs[2]+'.nrrd')
            writenifti(label_data, savepath + 'labels.nii.gz', info)
            ct_data, info = readnrrd(readpath+'img.nrrd')
            writenifti(ct_data, savepath+'img.nii.gz', info)
"""

