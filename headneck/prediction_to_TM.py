import numpy as np
import nibabel as nib
import os
import argparse
import glob
import pandas as pd
from scipy import ndimage
from scipy.ndimage import morphology
import scipy.io
from train import config as config_unet
from train_isensee2017 import config as config_isensee

def material_index():

	index_dict = {"Brainstem":62, "Mandible":42, "Parotid":71}
	index_dict = {k.lower():v for k,v in index_dict.items()}
	return index_dict

	"""
	index_dict = {"Air_exterior": 1, "Air_internal" : 2, "BloodA": 3, "Blood_vessels": 5, "Bones": 6, "Gray Matter": 7, "White matter": 8, "Cartilage" : 11, "Cerebellum" : 12,
				  "CSF" : 13, "Commissura_anterior" : 14, "Commissura_posterior" : 15, "Connective_tissue" : 16, "Cornea" : 17, "Ear_cartilage" : 19, "Ear_skin" : 20,
				  "Esophagus" : 22, "Eye_lens" : 23, "Air_esophagus" : 24, "Eye_Sclera" : 25, "Eye_vitreous_humor" : 26, "Fat": 27, "Hippocampus" : 31, "Hypophysis" : 32,
				  "Hypothalamus" : 33, "Intervertebral_disc" : 34, "Larynx" : 39, "Lung" : 41, "Mandible" : 42, "Marrow_red" : 43, "Medulla_oblongata" : 44, "Midbrain" : 46,
				  "Mucosa" : 47, "Muscle" : 48, "Nerve" : 49, "Pharynx" : 53, "Pinealbody" : 54, "Pons" : 55, "SAT" : 57, "Skin" : 58, "Skull" : 59, "Spinal cord" : 62, 
				  "Teeth" : 66, "Tendon_Ligament" : 67, "Thalamus" : 69, "Thyroid_gland" : 71, "Tongue" : 72, "Trachea" : 73, "Air_trachea"  : 74, "Vein" : 76, "Vertebrae" : 77,
				  "Tumor" : 80, "Water (debye-15C)" : 81}
	"""


def main():

	index_dict = material_index()
	prediction_dir = os.path.abspath("./headneck/prediction/")
	TM_dir = os.path.abspath("./headneck/tissue_matrices/")

	if not os.path.exists(TM_dir):
		os.makedirs(TM_dir)

	organ_dir = glob.glob(os.path.join(prediction_dir,"*"))[0]
	image_shape = np.array(config_isensee["image_shape"])

	subject_list = list()

	for case_folder in glob.glob(os.path.join(organ_dir,"*")):

		if os.path.isdir(case_folder):
			subject_list.append(os.path.basename(case_folder))

	for subject in subject_list:

		prediction = np.zeros(image_shape)

		for organ_folder in glob.glob(os.path.join(prediction_dir,"*")):
			organ = os.path.basename(organ_folder)
			index = index_dict.get(organ, 1)

			prediction_file = os.path.join(organ_folder, subject, "prediction.nii.gz")
			prediction_organ_image = nib.load(prediction_file)
			prediction_organ = prediction_organ_image.get_data()
			prediction_organ[prediction_organ == 1] = index

			prediction[prediction_organ>0] = 0 # removing overlay
			prediction = prediction + prediction_organ

		prediction[prediction==0] = 1 # changing background index to air_extrior
		scipy.io.savemat(os.path.join(TM_dir, "TM_subject_" + subject + '.mat'), mdict={'data': prediction})

if __name__ == "__main__":

	main()