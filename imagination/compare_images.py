"""
Home assignment Imagination, Saj, Veena, Payal
"""
from PIL import Image
import os
import logging


def compare_images(test_generated_image_folder_location, reff_image_folder_location, tolerance, name_of_log_file):

    """
    Function to compare the images in two folders
    Args:
        test_generated_image_folder_location:
        reff_image_folder_location:
        tolerance:
        name_of_log_file:

    Returns:

    """
    # Add the basic configuration for the log file.
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-5s %(levelname)-5s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        filename=name_of_log_file,
                        filemode='w')
    logger = logging.getLogger()
    summary = {}
    # Get the list of all files in test folder
    test_image_list = os.listdir(test_generated_image_folder_location)
    test_image_count = len(test_image_list)
    # Get the list of all files in ref folder
    ref_image_list = os.listdir(reff_image_folder_location)
    ref_image_count = len(ref_image_list)
    # Start a loop on all files in test folder
    for test_image in test_image_list:
        # Get the full path of files in test folder
        test_image_path = os.path.join(test_generated_image_folder_location, test_image)
        logger.info(f"Starting the comparison of test image file: {test_image_path}")
        # If same name files are present in ref folder and test folder
        if test_image in ref_image_list:
            # Get the full path of files in ref folder
            ref_image_path = os.path.join(reff_image_folder_location, test_image)
            logger.info(f"Corresponding reference image file: {ref_image_path}")
            # Open test image file
            test_img = Image.open(test_image_path)
            # Get the size of test image
            test_image_size = test_img.size
            logger.debug(f"Size of test image: {test_image_size}")
            # Open ref image file
            ref_img = Image.open(ref_image_path)
            # Get the size of ref image
            ref_image_size = ref_img.size
            logger.debug(f"Size of ref image: {ref_image_size}")
            # If the size of ref image and test image does not match
            if test_image_size != ref_image_size:
                # Resize the test image as ref image size
                logger.debug(f"Resizing test image with corresponding reference image size.")
                resized_test_img = test_img.resize(ref_image_size)
                # Remove the old test file
                os.remove(test_image_path)
                # Save the new test image file after resize
                resized_test_img.save(test_image_path)

            test_img.close()
            ref_img.close()
            logger.info(f"Ending the comparison of test image file: {test_image_path}")
        else:
            # If test image file is present but reference image file is not present.
            logger.info(f"Test image is present but corresponding reference image is not present: {test_image_path}")


compare_images("/Users/ngupta/Desktop/docs/new_jobs/imagination/veena/coding_test/Images/test_nik",
               "/Users/ngupta/Desktop/docs/new_jobs/imagination/veena/coding_test/Images/ref_nik",
               None, "compare_images.log")
