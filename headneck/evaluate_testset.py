import numpy as np
import nibabel as nib
import os
import glob
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from .utils import pickle_dump, pickle_load
from train_isensee2017 import config
from unet3d.prediction import run_validation_cases
from unet3d.data import write_data_to_file
from evaluate import get_background_mask, get_organ_mask, dice_coefficient

config["data_file"] = os.path.abspath("./headneck/prediction_test/headneck_data.h5")
config["test_file"] = os.path.abspath("./headneck/prediction_test/isensee_test_ids.pkl")
config["model_file"] = os.path.abspath("./headneck/isensee2017_test/isensee_2017_model.h5")

def fetch_test_data_files(return_subject_ids=False):
    test_data_files = list()
    subject_ids = list()
    for subject_dir in glob.glob(os.path.join(os.path.dirname(__file__), "data", "preprocessed_test", "*", "*")):
        subject_ids.append(os.path.basename(subject_dir))
        subject_files = list()
        for modality in config["training_modalities"] + ["truth"]:
            subject_files.append(os.path.join(subject_dir, modality + ".nii.gz"))
        test_data_files.append(tuple(subject_files))
    if return_subject_ids:
        return test_data_files, subject_ids
    else:
        return test_data_files

if not os.path.exists(config["data_file"]):
	training_files, subject_ids = fetch_test_data_files(return_subject_ids=True)

	write_data_to_file(training_files, config["data_file"], image_shape=config["image_shape"], subject_ids=subject_ids)

if not os.path.exists(config["test_file"]):
	test_list = list(range(len(subject_ids)))
	pickle_dump(test_list, config["test_file"])


prediction_dir = os.path.abspath("./headneck/prediction_test")

if not os.path.exists(prediction_dir):
	os.makedirs(prediction_dir)

run_validation_cases(validation_keys_file=config["test_file"],
   	                 model_file=config["model_file"],
       	             training_modalities=config["training_modalities"],
           	         labels=config["labels"],
               	     hdf5_file=config["data_file"],
               	  	 output_label_map=True,
                  	 output_dir=prediction_dir)

header = ("Background", "Mandible")
masking_functions = (get_background_mask, get_organ_mask)
rows = list()
prediction_path = "./headneck/prediction_test/"
for case_folder in glob.glob(prediction_path+"*/"):
    truth_file = os.path.join(case_folder, "truth.nii.gz")
    truth_image = nib.load(truth_file)
    truth = truth_image.get_data()
    prediction_file = os.path.join(case_folder, "prediction.nii.gz")
    prediction_image = nib.load(prediction_file)
    prediction = prediction_image.get_data()
    rows.append([dice_coefficient(func(truth), func(prediction))for func in masking_functions])
df = pd.DataFrame.from_records(rows, columns=header)
df.to_csv(prediction_path+"headneck_scores.csv")

scores = dict()
for index, score in enumerate(df.columns):
    values = df.values.T[index]
    scores[score] = values[np.isnan(values) == False]

plt.boxplot(list(scores.values()), labels=list(scores.keys()))
plt.ylabel("Dice Coefficient")
plt.savefig(prediction_path+"test_scores_boxplot.png")
plt.close()