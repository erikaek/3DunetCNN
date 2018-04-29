import os
import argparse

from train import config as config_unet
from train_isensee2017 import config as config_isensee
from unet3d.prediction import run_validation_cases


def main(args):

	prediction_dir = os.path.abspath("./headneck/prediction/"+args.gpu.lower())

	if not os.path.exists(prediction_dir):

		os.makedirs(prediction_dir)

	if args.gpu.lower() == "gpu0" || args.gpu.lower() == "gpu1":

		run_validation_cases(validation_keys_file=config_isensee["validation_file"],
        	                 model_file=config_isensee["model_file"],
            	             training_modalities=config_isensee["training_modalities"],
                	         labels=config_isensee["labels"],
                    	     hdf5_file=config_isensee["data_file"],
                    	  	 output_label_map=True,
                         	 output_dir=prediction_dir)
	else:

		raise Exception("ERROR: Unvalid gpu! Enter gpu0 OR gpu1")




if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("gpuu", help="enter gpu: gpu0 OR gpu1")
	args = parser.parse_args()

	main(args)
    	
