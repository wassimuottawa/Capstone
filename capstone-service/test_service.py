import os
import unittest
from datetime import time
import shutil

import service

from unittest.mock import patch


class TestService(unittest.TestCase):

    @patch('service.get_folders_in_path')
    def test_get_folders_in_path(self, mock_path):
        mock_path.return_value = ['archive', 'run 1', 'run3', 'tests']
        try:
            service.get_folders_in_path()
        except TypeError:
            pass
        self.assertEqual(service.get_folders_in_path('root'), ['archive', 'run 1', 'run3', 'tests'])

    def test_get_folders_by_run(self):
        try:
            service.get_folders_by_run()
        except TypeError:
            pass
        self.assertEqual(service.get_folders_by_run('run 1'), {'1': ['0001', '0004'], '2': ['0001', '0003'],
                                                               '3': ['0005', '0012', '0015'], '5': ['0003'],
                                                               '6': ['0007'], '7': ['0001', '0009'],
                                                               '8': ['0005', '0006'], '9': ['0007']})

    def test_folder_exists(self):
        try:
            service.folder_exists()
        except TypeError:
            pass
        self.assertEqual(service.folder_exists('run 1', '1'), True)
        self.assertNotEqual(service.folder_exists('run 1', '10'), True)

    @patch('service.get_image_file')
    def test_get_image_file(self, mock_get):
        run = 'run 1'
        folder = '2'
        tracklet = '0003'
        file_name = '1629264814.4908354.png'
        mock_get.return_value = None
        self.assertEqual(service.get_image_file(run, folder, tracklet, file_name), None)

    def test_folder_contains_image(self):
        try:
            service.folder_contains_image()
        except TypeError:
            pass
        self.assertEqual(service.folder_contains_image('run 1', '1', '0001'), True)
        self.assertNotEqual(service.folder_contains_image('run 1', '9', '0007'), False)
        self.assertEqual(service.folder_contains_image('run 1', '7', '0009'), True)

    @patch('service.get_image_names')
    def test_get_image_names(self, mock_images):
        mock_images.return_value = {'0001': ['1629264807.9152288.png',
                                             '1629264807.9463031.png',
                                             '1629264807.9777446.png',
                                             '1629264809.97505.png'],
                                    '0004': ['1629264809.2087257.png',
                                             '1629264809.388927.png',
                                             '1629264809.4852278.png',
                                             '1629264809.516625.png',
                                             '1629264809.5645351.png',
                                             '1629264809.5972645.png',
                                             '1629264809.931977.png',
                                             '1629264810.0094361.png',
                                             '1629264810.39205.png']}
        try:
            service.get_image_names()
        except TypeError:
            pass
        self.assertEqual(service.get_image_names({'run': 'run 1', 'folder': '1'}), {'0001': ['1629264807.9152288.png',
                                                                                             '1629264807.9463031.png',
                                                                                             '1629264807.9777446.png',
                                                                                             '1629264809.97505.png'],
                                                                                    '0004': ['1629264809.2087257.png',
                                                                                             '1629264809.388927.png',
                                                                                             '1629264809.4852278.png',
                                                                                             '1629264809.516625.png',
                                                                                             '1629264809.5645351.png',
                                                                                             '1629264809.5972645.png',
                                                                                             '1629264809.931977.png',
                                                                                             '1629264810.0094361.png',
                                                                                             '1629264810.39205.png']})

    def test_is_image(self):
        try:
            service.is_image()
        except TypeError:
            pass
        self.assertEqual(service.is_image("123.456.png"), True)
        self.assertEqual(service.is_image("123.456.jpg"), False)
        self.assertNotEqual(service.is_image("an_image"), True)

    @patch('service.get_image_names_in_path')
    def test_get_image_names_in_path(self, mocked_images_in_path):
        mocked_images_in_path.return_value = ['1629264809.2087257.png',
                                              '1629264809.4852278.png',
                                              '1629264809.516625.png',
                                              '1629264809.5645351.png',
                                              '1629264809.5972645.png',
                                              '1629264809.931977.png',
                                              '1629264810.0094361.png',
                                              '1629264810.0450258.png',
                                              '1629264810.0793295.png',
                                              '1629264810.1243467.png',
                                              '1629264810.159293.png',
                                              '1629264810.39205.png',
                                              '1629264810.4277048.png']
        try:
            service.get_image_names_in_path()
        except TypeError:
            pass
        self.assertEqual(service.get_image_names_in_path('run 1', '8', '0005'), ['1629264809.2087257.png',
                                                                                 '1629264809.4852278.png',
                                                                                 '1629264809.516625.png',
                                                                                 '1629264809.5645351.png',
                                                                                 '1629264809.5972645.png',
                                                                                 '1629264809.931977.png',
                                                                                 '1629264810.0094361.png',
                                                                                 '1629264810.0450258.png',
                                                                                 '1629264810.0793295.png',
                                                                                 '1629264810.1243467.png',
                                                                                 '1629264810.159293.png',
                                                                                 '1629264810.39205.png',
                                                                                 '1629264810.4277048.png'])

        self.assertNotEqual(service.get_image_names_in_path('run 1', '3', '0012'), ['1629264810.0094361.png',
                                                                                    '1629264810.0450258.png',
                                                                                    '1629264810.0793295.png',
                                                                                    '1629264810.159293.png',
                                                                                    '1629264811.123456.png'])

    @patch('service.get_runs')
    def test_get_runs(self, mock_result):
        mock_result.return_value = ['run 1', 'run3', 'tests']
        try:
            service.get_runs()
        except TypeError:
            pass
        self.assertEqual(service.get_runs(), ['run 1', 'run3', 'tests'])

    @patch('service.delete_files')
    def test_delete_files(self, mock_del):
        payload = {
            "run": "run 1",
            "mapping": {
                "1/0001": ["1629264809.97505.png"]}
        }
        mock_del.return_value = 'root/archive/1629264809.97505.png'
        self.assertEqual((service.delete_files(payload)), 'root/archive/1629264809.97505.png')

    @patch('service.move')
    def test_move(self, mock_move):
        values = {
            "run": "run 1",
            "mapping": {
                "1/0004": ["1629264809.388927.png"]
            },
            "destination_path": "file_moved"
        }
        mock_move.return_value = True
        self.assertEqual(service.move(values), True)

    @patch('service.move_files')
    def test_move_files(self, mock_files_moved):
        run = 'run 1'
        mapping = {
            "5/0003": ["1629264811.767846.png", "1629264811.7347393.png", "1629264813.1253777.png",
                       "1629264813.1591573.png", "1629264814.5563.png", "1629264814.2895732.png",
                       "1629264814.3458185.png", "1629264814.4908354.png", "1629264814.5914614.png",
                       "1629264816.65119.png", "1629264816.548322.png", "1629264816.684646.png",
                       "1629264816.778424.png"]
        }
        destination = "root/run 1/10"
        mock_files_moved.return_value = True
        self.assertEqual(service.move_files(run, mapping, destination), True)

    def test_get_time_from_file_name(self):
        try:
            service.get_time_from_file_name()
        except TypeError:
            pass
        self.assertEqual(service.get_time_from_file_name("1629264807.9777446.png"), time(5, 33, 27, 977745))  # GMT +4
        self.assertEqual(service.get_time_from_file_name("1629264807.9463031.png"), time(5, 33, 27, 946303))  # GMT +4
        self.assertEqual(service.get_time_from_file_name("1629264813.1253777.png"), time(5, 33, 33, 125378))  # GMT +4

    def test_is_in_time_range(self):
        try:
            service.is_in_time_range()
        except TypeError:
            pass
        self.assertEqual(service.is_in_time_range("1629264807.622246.png", time(5, 0), time(6, 0)), True)  # GMT +4
        self.assertEqual(service.is_in_time_range("1629264810.0094361.png", time(2, 0), time(3, 0)), False)

    def test_str_to_time(self):
        try:
            service.str_to_time()
        except TypeError:
            pass
        self.assertEqual(service.str_to_time('12:00'), time(12, 0))
        self.assertNotEqual(service.str_to_time('11:50'), time(10, 50))


if __name__ == '__main__':
    unittest.main()
