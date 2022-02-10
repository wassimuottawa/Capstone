import os
import shutil
import unittest
from datetime import time

import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        test_root_path = 'test root'
        list_of_options = ['test archive', 'test run 1']
        if not os.path.exists(test_root_path):
            os.makedirs(test_root_path)
            for options in list_of_options:
                os.makedirs(test_root_path + "/" + options)
            for i in range(2):
                os.makedirs(
                    test_root_path + "/" + "test run 1" + "/" + "000000000" + str(i + 1) + "/" + "00000000000" + str(
                        i + 1))
        dummy_images_set_1 = ['cam1;x_306;y_205;w_167;h_235;1636565415019736200.png',
                              'cam1;x_305;y_204;w_167;h_234;1636565415019736201.png',
                              'cam1;x_304;y_203;w_167;h_233;1636565415019736202.png',
                              'cam1;x_303;y_202;w_167;h_232;1636565415019736203.png',
                              'cam1;x_302;y_201;w_167;h_231;1636565415019736204.png',
                              'cam1;x_301;y_200;w_167;h_230;1636565415019736205.png',
                              'cam1;x_300;y_199;w_167;h_229;1636565415019736206.png',
                              'cam1;x_299;y_198;w_167;h_228;1636565415019736207.png']

        dummy_images_set_2 = ['cam1;x_306;y_205;w_167;h_227;1636565415019736199.png',
                              'cam1;x_305;y_204;w_167;h_226;1636565415019736198.png',
                              'cam1;x_304;y_203;w_167;h_225;1636565415019736197.png',
                              'cam1;x_303;y_202;w_167;h_224;1636565415019736196.png',
                              'cam1;x_302;y_201;w_167;h_223;1636565415019736195.png',
                              'cam1;x_301;y_200;w_167;h_222;1636565415019736194.png',
                              'cam1;x_300;y_199;w_167;h_221;1636565415019736193.png',
                              'cam1;x_299;y_198;w_167;h_220;1636565415019736192.png']

        for images in dummy_images_set_1:
            with open(os.path.join(test_root_path + "/" + "test run 1" + "/" + "0000000001" + "/" + "000000000001",
                                   images),
                      'w') as files:
                files.write("written")

        for other_images in dummy_images_set_2:
            with open(os.path.join(test_root_path + "/" + "test run 1" + "/" + "0000000002" + "/" + "000000000002",
                                   other_images),
                      'w') as files:
                files.write("written")

    def test_get_folders_in_path(self):
        try:
            utils.get_folders_in_path()
        except TypeError:
            pass
        self.assertEqual(utils.get_folders_in_path('test root'), ['test archive', 'test run 1'])

    def test_folder_contains_image(self):
        try:
            utils.folder_contains_image()
        except TypeError:
            pass
        self.assertEqual(utils.folder_contains_image('test root/test run 1/0000000001/000000000001'), True)
        self.assertEqual(utils.folder_contains_image('test root/test run 1/0000000002/000000000002'), True)
        self.assertNotEqual(utils.folder_contains_image('test root/test run 1/0000000001'), True)

    def test_is_image(self):
        try:
            utils.is_image()
        except TypeError:
            pass
        self.assertEqual(utils.is_image('cam1;x_306;y_205;w_167;h_227;1636565415019736199.png'), True)
        self.assertNotEqual(utils.is_image('123.jpg'), True)

    def test_get_image_names_in_path(self):
        try:
            utils.get_image_names_in_path()
        except TypeError:
            pass
        path = 'test root/test run 1/0000000001/000000000001'
        self.assertEqual(utils.get_image_names_in_path(path), ['cam1;x_299;y_198;w_167;h_228;1636565415019736207.png',
                                                               'cam1;x_300;y_199;w_167;h_229;1636565415019736206.png',
                                                               'cam1;x_301;y_200;w_167;h_230;1636565415019736205.png',
                                                               'cam1;x_302;y_201;w_167;h_231;1636565415019736204.png',
                                                               'cam1;x_303;y_202;w_167;h_232;1636565415019736203.png',
                                                               'cam1;x_304;y_203;w_167;h_233;1636565415019736202.png',
                                                               'cam1;x_305;y_204;w_167;h_234;1636565415019736201.png',
                                                               'cam1;x_306;y_205;w_167;h_235;1636565415019736200.png'])

    def test_get_time_from_file_name(self):
        try:
            utils.get_time_from_file_name()
        except TypeError:
            pass
        self.assertEqual(utils.get_time_from_file_name('cam1;x_299;y_198;w_167;h_228;1636565415019736207.png'),
                         time(16, 30, 15, 19736))  # Added hour +4 before push
        self.assertEqual(utils.get_time_from_file_name('cam1;x_301;y_200;w_167;h_222;1836565415025736194.png'),
                         time(13, 3, 35, 25736))  # Added hour +4 before push

    def test_is_in_time_range(self):
        try:
            utils.is_in_time_range()
        except TypeError:
            pass
        self.assertEqual(utils.is_in_time_range('cam1;x_299;y_198;w_167;h_228;1636565415019736207.png', None, None),
                         True)
        self.assertEqual(
            utils.is_in_time_range('cam1;x_299;y_198;w_167;h_228;1636565415019736207.png', time(16, 0), time(17, 0)),
            True)  # Added hour +4 before push

    def test_str_to_time(self):
        try:
            utils.str_to_time()
        except TypeError:
            pass
        self.assertEqual(utils.str_to_time('12:00'), time(12, 0))
        self.assertNotEqual(utils.str_to_time('11:50'), time(10, 50))

    def test_sort_images_by_time(self):
        try:
            utils.sort_images_by_time()
        except TypeError:
            pass
        list_images = ['cam1;x_299;y_198;w_167;h_218;1636565415019736202.png',
                       'cam1;x_300;y_199;w_167;h_229;1636565415019736206.png',
                       'cam1;x_301;y_200;w_167;h_280;1636565415019736200.png',
                       'cam1;x_302;y_201;w_167;h_199;1636565415019736201.png',
                       'cam1;x_303;y_202;w_167;h_150;1636565415019736199.png']
        self.assertEqual(utils.sort_images_by_time(list_images),
                         ['cam1;x_299;y_198;w_167;h_218;1636565415019736202.png',
                          'cam1;x_300;y_199;w_167;h_229;1636565415019736206.png',
                          'cam1;x_301;y_200;w_167;h_280;1636565415019736200.png',
                          'cam1;x_302;y_201;w_167;h_199;1636565415019736201.png',
                          'cam1;x_303;y_202;w_167;h_150;1636565415019736199.png'])

    def test_get_error_name(self):
        try:
            utils.get_error_name()
        except TypeError:
            pass
        self.assertEqual(utils.get_error_name(AssertionError), 'type')
        self.assertEqual(utils.get_error_name(AttributeError), 'type')

    def tearDown(self):
        shutil.rmtree('test root')


if __name__ == '__main__':
    unittest.main()
