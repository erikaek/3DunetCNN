import numpy as np
import nibabel as nib
import os
import argparse
import glob
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from scipy.ndimage import morphology
import scipy.io
from evaluate import dice_coefficient, get_organ_mask


def surfd(input1, input2, sampling=1, connectivity=1):
    
    input_1 = np.atleast_1d(input1.astype(np.bool))
    input_2 = np.atleast_1d(input2.astype(np.bool))

    conn = morphology.generate_binary_structure(input_1.ndim, connectivity)

    S = np.logical_xor(input_1, morphology.binary_erosion(input_1, conn))  
    Sprime = np.logical_xor(input_2, morphology.binary_erosion(input_2, conn))  

    dta = morphology.distance_transform_edt(~S,sampling)
    dtb = morphology.distance_transform_edt(~Sprime,sampling)
    
    sds = np.concatenate([np.ravel(dta[Sprime!=0]), np.ravel(dtb[S!=0])])
       
    
    return sds


def main(args):

	threshold = 100 # excluding connected components of volume smaller than

	dice = list()
	hdmax = list()
	hd95 = list()
	cm = list()
	prediction_path = os.path.abspath("./headneck/prediction/")

	if not os.path.exists(metrics_path):
		os.makedirs(metrics_path)

	# removes outlier data and calculates metric values for the predicted segmentation
	for case_folder in glob.glob(prediction_path+"*/"):
		truth_file = os.path.join(case_folder, "truth.nii.gz")
		truth_image = nib.load(truth_file)
		truth = truth_image.get_data()
		prediction_file = os.path.join(case_folder, "prediction.nii.gz")
		prediction_image = nib.load(prediction_file)
		prediction = prediction_image.get_data()

		labeled_pred, num_features = scipy.ndimage.measurements.label(prediction, structure=np.ones([3, 3, 3]), output=truth.dtype)
		unique, counts = np.unique(labeled_pred, return_counts=True)


		for i_lab in range(len(unique)):
			if counts[i_lab] < threshold:
				labeled_pred[labeled_pred==unique[i_lab]] = 0

		labeled_pred[labeled_pred>1] = 1
		prediction = labeled_pred	

		new_prediction_image = nib.Nifti1Image(prediction, prediction_image.affine, prediction_image.header)
		nib.save(new_prediction_image, prediction_file)

		dice.append(dice_coefficient(truth,prediction))


		surface_distance = surfd(prediction, truth, np.asarray(truth_image.header.get_zooms()),2)
		hd95.append(np.percentile(surface_distance,95))
		hdmax.append(surface_distance.max())
		cm.append(surface_distance.mean())

	dice = np.asarray(dice)
	hd95 = np.asarray(hd95)
	hdmax = np.asarray(hdmax)
	cm = np.asarray(cm)

	print("Dice:")
	print(dice)
	print("HD95:")
	print(hd95)
	print("HD:")
	print(HD)
	print("CM:")
	print(cm)


if __name__ == "__main__":

	main()
