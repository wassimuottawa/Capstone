import unittest
from unittest import result
from datetime import time
import service

class TestService(unittest.TestCase):
    def test_get_folders_in_path(self):
        try:
            service.get_folders_in_path()
        except TypeError:
            pass
        self.assertEqual(service.get_folders_in_path('root/run3'),['cam0', 'cam1'])

    def test_get_folders_by_run(self):
        try:
            service.get_folders_by_run()
        except TypeError:
            pass
        self.assertEqual(service.get_folders_by_run('run3'),set(['1']))
        self.assertNotEqual(service.get_folders_by_run('run3'),set(['1','2']))
        self.assertEqual(service.get_folders_by_run('run 1'),set(['11', '10', '13', '12', '15', '14', '1', '3', '2', '5', '4', '7', '6', '9', '8']))

    def test_get_cams(self):
        try:
            service.get_cams()
        except TypeError:
            pass
        self.assertEqual(service.get_cams('run 1'),['cam0', 'cam1'])

    def test_file_exists(self):
        try:
            service.file_exists()
            service.file_exists('run3','cam0','1')
            service.file_exists('run3','cam0','test1.png')
            service.file_exists('run3','1','test1.png')
            service.file_exists('cam0','1','test1.png')
        except TypeError:
            pass
        self.assertEqual(service.file_exists('run3','cam0','1','test1.png'),True)
        self.assertEqual(service.file_exists('run2','cam0','1','test1.png'),False)
        self.assertEqual(service.file_exists('run3','cam2','1','test1.png'),False)
        self.assertEqual(service.file_exists('run3','cam0','2','test2.png'),False)

    def test_folder_exists(self):
        try:
            service.folder_exists()
            service.folder_exists('run5','cam1')
            service.folder_exists('run3','test1.png')
            service.folder_exists('cam1','test1.png')
        except TypeError:
            pass
        self.assertEqual(service.folder_exists('run3','cam0','1'),True)
        self.assertEqual(service.folder_exists('run2','cam0','1'),False)
        self.assertEqual(service.folder_exists('run3','cam2','1'),False)
        self.assertEqual(service.folder_exists('run3','cam0','2'),False)

    def test_get_file(self):
        try:
            service.get_file()
            service.get_file('run5','cam1','test1.png')
            service.get_file('run3','cam2','test1.png')
            service.get_file('run3','cam1','test4.png')
        except TypeError:
            pass
        self.assertEqual(service.get_file('run3','cam1','test1.png'),None)

    def test_not_empty(self):
        try:
            self.assertEqual(service.not_empty('run3','cam0','2'))
        except OSError:
            pass
        self.assertEqual(service.not_empty('run3','cam1','1'),True)
        self.assertEqual(service.not_empty('run3','cam0','1'),True)

    def test_get_image_names(self):
        try:
            service.get_image_names()
        except TypeError:
            pass
        self.assertEqual(service.get_image_names({'run': 'run3', 'folder': '1'}),{'test1.png', 'test2.png'})
        self.assertEqual(service.get_image_names({'run': 'run 1', 'folder': '8'}),{'1629264810.0094361.png', '1629264809.516625.png', '1629264811.702891.png', '1629264810.39205.png', '1629264809.931977.png', '1629264810.159293.png', '1629264809.4852278.png', '1629264810.0450258.png', '1629264809.2087257.png', '1629264811.767846.png', '1629264811.7347393.png', '1629264810.0793295.png', '1629264809.5972645.png', '1629264810.4277048.png', '1629264810.1243467.png', '1629264809.5645351.png'})
        self.assertNotEqual(service.get_image_names({'run': 'run 1', 'folder': '7'}),service.get_image_names({'run': 'run 1', 'folder': '8'}))
    
    def test_is_image(self):
        try:
            service.is_image()
        except TypeError:
            pass
        self.assertIsNotNone(service.is_image("root/run3/cam0/test1.png"))
        self.assertEqual(service.is_image("root/run3/cam0/test1.png"),True)
        self.assertEqual(service.is_image("root/run3/cam0/test1"),False)

    def test_get_runs(self):
        try:
            service.get_runs() # Common to get ValueError is no 'archive' folder exists in root directory
        except ValueError:
            pass

    # def test_delete_files(self):

    # def test_move(self):

    # def test_move_files(self):

    # def test_get_time_from_file_name(self):

    # def test_is_in_time_range(self):
        
    # def test_str_to_time(self):

if __name__ == '__main__':
    unittest.main()
