import compare_images

TEST_DIR_PATH = "/Users/ngupta/Desktop/docs/new_jobs/imagination/veena/coding_test/Images/test_generated_images"
REF_DIR_PATH = "/Users/ngupta/Desktop/docs/new_jobs/imagination/veena/coding_test/Images/reference_images"

compare_images.compare_images(TEST_DIR_PATH, REF_DIR_PATH, 10, "compare_images.log")
