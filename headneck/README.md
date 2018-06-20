## Data Management

### Downloading Data

Head and neck data from the MICCAI 2015 Auto-segmentation challenge (http://www.imagenglab.com/wiki/mediawiki/index.php?title=2015_MICCAI_Challenge) can be found here: (http://www.imagenglab.com/newsite/pddca/ )

### Reformatting Data

This data comes in the .nrrd format. This needs to be converted to nifti for this network and this is done by:

	cd headneck
	python conversion.py

where you need to change the data_path-parameter according to the location of the downloaded data. This code is currently adjusted to training on binary organs due to the fact that the data is not fully annotated. Therefore, you also need to select an organ by changing the organ-parameter. It is to be named according to the organ names within the structures-folder within the subject folders in the downloaded data folders.

### Preprocessing Data

To preprocess the data use:

	python
	from preprocess import convert_data
	convert_data("data/original, "data/preprocessed")

## Training

It is recommended that you train the network using:

	python headneck/train_isensee2017.py

You can also use the original 3D U-net implementation in train.py. The main difference in the files in this folder compared to the training files in the brats-folder is the data augmentation used. If you would like the same type of data augmentation also for the brats data you can change the corresponding training files accordingly. 

### Prediction

To predict the segmentation of the validation data set use:

	python headneck/predict.py

This script saves the prediction of the validations sets along with the original image set and segmentation in a prediction folder. To derive loss plots and boxplots over the obtained dice values use:

	python headneck/evaluate.py

which saves corresponding png-images in the same prediction folder.

To instead predict and evaluate a test set you can use:

	python headneck/evaluate_testset.py

Reformat and preprocess the test data as described above with the only difference in the folder name of the preprocessed data. Use instead:

	convert_data("data/original, "data/preprocessed_test")

The obtained prediction and evaluation will be saved in a prediction_test-folder.

## Postprocessing

You can also remove outlier points in the final prediction through a postprocessing step by running:

	python headneck/postprecess.py

Here, you can change the prediction_path-parameter according to if you want to consider the validation or the test set. Default is the validation set. This script also calculates the dice values, 95th percentile- and maximum Hausdorff distance and the contour mean distance for each data set.
