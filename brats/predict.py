import os
import argparse

from train import config as config_unet
from train_isensee2017 import config as config_isensee
from unet3d.prediction import run_validation_cases


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("mode", help="enter model mode: unet OR isensee")
	args = parser.parse_args()
	
	if args.mode.lower() == 'unet':

    	prediction_dir = os.path.abspath("./unet/prediction")
    	run_validation_cases(validation_keys_file=config_unet["validation_file"],
        	                 model_file=config_unet["model_file"],
            	             training_modalities=config_unet["training_modalities"],
                	         labels=config_unet["labels"],
                    	     hdf5_file=config_unet["data_file"],
                    	  	 output_label_map=True,
                         	 output_dir=prediction_dir)

    elif args.mode.lower() == 'isensee':

    	prediction_dir = os.path.abspath("./isensee2017/prediction")
    	run_validation_cases(validation_keys_file=config_isensee["validation_file"],
        	                 model_file=config_isensee["model_file"],
            	             training_modalities=config_isensee["training_modalities"],
                	         labels=config_isensee["labels"],
                    	     hdf5_file=config_isensee["data_file"],
                    	  	 output_label_map=True,
                         	 output_dir=prediction_dir)

    else : 

    	raise Exception('Unvalid model mode! Enter unet OR isensee')




if __name__ == "__main__":
    main()
