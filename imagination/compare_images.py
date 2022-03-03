"""
Home assignment Imagination, Saj, Veena, Payal
"""
from PIL import Image
import os
import logging
import threading


# max THREAD_COUNT = 100
THREAD_COUNT = 5
# max batch FILES_PER_THREAD = 1000
FILES_PER_THREAD = 2
TEST_DIR_PATH = ""
REF_DIR_PATH = ""
LOGGER = None
RESIZED_FILES_LIST = []
RESIZED_FILES_COUNT = 0
TOLERANCE = 0
DIFF = 'diff'


def resize_image(file_name_list, thread_batch_number):
    for file_name in file_name_list:
        # Get the full path of files in test folder
        test_image_path = os.path.join(TEST_DIR_PATH, file_name)
        LOGGER.info(f"Thread: {thread_batch_number}: Starting the comparison of test image file: {file_name}")
        # Get the full path of files in ref folder
        ref_image_path = os.path.join(REF_DIR_PATH, file_name)
        # Open test image file
        test_img = Image.open(test_image_path)
        # Get the size of test image
        test_image_size = test_img.size
        LOGGER.debug(f"Thread: {thread_batch_number}: Size of test image {file_name}: {test_image_size}")
        # Open ref image file
        ref_img = Image.open(ref_image_path)
        # Get the size of ref image
        ref_image_size = ref_img.size
        LOGGER.debug(f"Thread: {thread_batch_number}: Size of ref image {file_name}: {ref_image_size}")
        # If the size of ref image and test image does not match
        # If size of both files are same then no action is required, solution of point number 3
        if test_image_size != ref_image_size:
            # Resize the test image as ref image size
            LOGGER.debug(f"Thread: {thread_batch_number}: Resizing {file_name} with corresponding reference image size.")
            #RESIZED_FILES_LIST.append(file_name)
            resized_test_img = test_img.resize(ref_image_size)
            global RESIZED_FILES_COUNT
            RESIZED_FILES_COUNT += 1
            # Remove the old test file
            os.remove(test_image_path)
            # Save the new test image file after resize
            resized_test_img.save(test_image_path)
            resized_test_img.close()
            #pixel_to_pixel_comparison(file_name)
        test_img.close()
        ref_img.close()
        LOGGER.info(f"Ending the comparison of test image file: {file_name}")


def create_threads_for_file_resize(list_common_files):
    start = 0
    end = FILES_PER_THREAD
    thread_batch_count = len(list_common_files) // (THREAD_COUNT * FILES_PER_THREAD) + 1
    for thread_batch_number in range(thread_batch_count):
        thread_list = []
        for _ in range(THREAD_COUNT):
            temp_thread = threading.Thread(target=resize_image, args=[list_common_files[start:end], thread_batch_number])
            thread_list.append(temp_thread)
            temp_thread.start()
            start = end
            end = end + FILES_PER_THREAD
        for i in range(THREAD_COUNT):
            thread_list[i].join()


def log_files_absent_in_reference_folder(test_image_list, ref_image_list):
    """
    Log file name that are present in test folder but not is reference folder.
    Log file name that are present in ref folder but not is test folder.
    return : list of common files.

    """
    set_test_images = set(test_image_list)
    set_ref_images = set(ref_image_list)
    # Solution of point number: 5
    LOGGER.info("File names that are present in test folder but not in reference folder:")
    LOGGER.info(set_test_images - set_ref_images)
    LOGGER.info("File names that are present in reference folder but not in test folder:")
    LOGGER.info(set_ref_images - set_test_images)
    # Solution of point number 1
    return list(set_test_images & set_ref_images)


def pixel_to_pixel_comparison(file_name):
    #for image_file in file_list:

    test_image_path = os.path.join(TEST_DIR_PATH, file_name)
    ref_image_path = os.path.join(REF_DIR_PATH, file_name)
    with Image.open(test_image_path) as test_image:
        with Image.open(ref_image_path) as ref_image:
            test_image_pixels = test_image.load()
            ref_image_pixels = ref_image.load()
            for y in range(test_image.height):
                for x in range(test_image.width):
                    ref_value_r = ref_image_pixels[x, y][0]
                    ref_value_g = ref_image_pixels[x, y][1]
                    ref_value_b = ref_image_pixels[x, y][2]
                    test_value_r = test_image_pixels[x, y][0]
                    test_value_g = test_image_pixels[x, y][1]
                    test_value_b = test_image_pixels[x, y][2]
                    lower_limits = (int(ref_value_r - TOLERANCE * 0.01 * ref_value_r),
                                    int(ref_value_g - TOLERANCE * 0.01 * ref_value_g),
                                    int(ref_value_b - TOLERANCE * 0.01 * ref_value_b))
                    upper_limits = (int(ref_value_r + TOLERANCE * 0.01 * ref_value_r),
                                    int(ref_value_g + TOLERANCE * 0.01 * ref_value_g),
                                    int(ref_value_b + TOLERANCE * 0.01 * ref_value_b))
                    if test_value_r < lower_limits[0] or \
                       test_value_g < lower_limits[1] or \
                       test_value_b < lower_limits[2] or \
                       test_value_r > upper_limits[0] or \
                       test_value_g > upper_limits[1] or \
                       test_value_b > upper_limits[2]:
                        copy_test_image = test_image.copy()
                        copy_test_image.save(os.path.join(TEST_DIR_PATH, f"{DIFF}{file_name}"))
                        copy_test_image.close()


def compare_images(test_generated_image_folder_location,
                   reff_image_folder_location,
                   tolerance,
                   name_of_log_file):

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
    logging.getLogger("PIL.Image").setLevel(logging.WARNING)
    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-5s %(levelname)-5s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        filename=name_of_log_file,
                        filemode='w')
    logger = logging.getLogger()
    global LOGGER
    LOGGER = logger
    logger.info(f"Test image directory path: {test_generated_image_folder_location}")
    logger.info(f"Reference image directory path: {reff_image_folder_location}")
    global TEST_DIR_PATH
    TEST_DIR_PATH = test_generated_image_folder_location
    global REF_DIR_PATH
    REF_DIR_PATH = reff_image_folder_location
    global TOLERANCE
    TOLERANCE = tolerance
    summary = {}
    # Get the list of all files in test folder
    test_image_list = os.listdir(test_generated_image_folder_location)
    # Get the list of all files in ref folder
    ref_image_list = os.listdir(reff_image_folder_location)
    # Log the files present in test folder but not in reference folder
    # Solution of point # 5
    list_common_files = log_files_absent_in_reference_folder(test_image_list,
                                                             ref_image_list)
    create_threads_for_file_resize(list_common_files)
    LOGGER.info(f"RESIZED_FILES_COUNT: {RESIZED_FILES_COUNT}")

# Test file content to test above code.
compare_images("/Users/ngupta/Desktop/docs/new_jobs/imagination/veena/coding_test/Images/test_generated_images",
               "/Users/ngupta/Desktop/docs/new_jobs/imagination/veena/coding_test/Images/reference_images",
               10, "compare_images.log")
