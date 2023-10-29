import unittest
import tempfile
import os
import shutil
from datetime import datetime, timedelta
from rm_old_folders import find_old_folders, delete_folders

class TestScript(unittest.TestCase):

    def setUp(self):
        # Create a temporary test directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the temporary test directory
        shutil.rmtree(self.test_dir)

    def create_test_folders(self, folder_names):
        # Create test folders with specified names
        for folder_name in folder_names:
            folder_path = os.path.join(self.test_dir, folder_name)
            os.makedirs(folder_path)
            # Set the modification time of the folder to make it older
            folder_date = datetime.strptime(folder_name, "%Y%m%d_%H%M%SZ")
            os.utime(folder_path, (folder_date.timestamp(), folder_date.timestamp()))

    def test_find_and_delete_old_folders(self):
        # Create test folders with specific timestamps
        test_folder_names = ["20231015_090000Z", "20231101_120000Z", "20231120_150000Z"]
        self.create_test_folders(test_folder_names)

        # Run the find_old_folders function
        old_folders = find_old_folders(self.test_dir, n_days=15)

        # Check that the correct folders are identified as old
        self.assertCountEqual(old_folders, test_folder_names[0:2])

        # Delete old folders
        delete_folders(self.test_dir, old_folders)

        # Check that the old folders are deleted
        for folder_name in old_folders:
            folder_path = os.path.join(self.test_dir, folder_name)
            self.assertFalse(os.path.exists(folder_path))

    def test_handle_folders_not_matching_format(self):
        # Create test folders with both valid and invalid names
        test_folder_names = ["20231015_090000Z", "invalid_folder", "20231101_120000Z", "another_invalid"]
        self.create_test_folders(test_folder_names)

        # Run the find_old_folders function
        old_folders = find_old_folders(self.test_dir, n_days=15)

        # Check that only valid folders are identified as old
        self.assertCountEqual(old_folders, ["20231015_090000Z", "20231101_120000Z"])

        # Delete old folders
        delete_folders(self.test_dir, old_folders)

        # Check that the old folders are deleted
        for folder_name in old_folders:
            folder_path = os.path.join(self.test_dir, folder_name)
            self.assertFalse(os.path.exists(folder_path))

if __name__ == '__main__':
    unittest.main()
