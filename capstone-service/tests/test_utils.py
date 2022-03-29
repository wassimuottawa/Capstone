import os
import shutil
import unittest
from datetime import time
from recordclass import recordclass


import utils

Range = recordclass('Range', 'start end')


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
        dummy_images_set_1 = ["cam1;x_480;y_79;w_53;h_172;1636570203689895900.png",
		                    "cam1;x_468;y_78;w_50;h_178;1636570203799268800.png",
                            "cam1;x_403;y_78;w_98;h_177;1636570204127382400.png",
		                    "cam1;x_444;y_81;w_59;h_174;1636570203908638900.png",
		                    "cam1;x_421;y_81;w_77;h_164;1636570204018009000.png",
                            "cam1;x_483;y_84;w_70;h_168;1636570203471151300.png",
                            "cam1;x_480;y_83;w_65;h_167;1636570203580522800.png"]

        dummy_images_set_2 = ["cam1;x_195;y_65;w_58;h_163;1636570206424179900.png",
                            "cam1;x_171;y_63;w_57;h_142;1636570206986659800.png",
		                    "cam1;x_182;y_64;w_60;h_143;1636570206642920400.png",
                            "cam1;x_188;y_65;w_56;h_148;1636570206533550500.png",
		                    "cam1;x_170;y_65;w_61;h_144;1636570206877291100.png",
                            "cam1;x_165;y_64;w_56;h_133;1636570207096032500.png",
		                    "cam1;x_165;y_64;w_56;h_134;1636570207205401700.png"]

        for images in dummy_images_set_1:
            with open(os.path.join(test_root_path, "test run 1", "0000000001", "000000000001", images), 'w') as files:
                files.write("written")

        for other_images in dummy_images_set_2:
            with open(os.path.join(test_root_path, "test run 1", "0000000002", "000000000002", other_images), 'w') as files:
                files.write("written")


    def test_get_folders_in_path(self):
        try:
            utils.get_folders()
        except TypeError:
            pass
        self.assertEqual(set(utils.get_folders('test root')), set(['test run 1', 'test archive']))


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
        self.assertEqual(set(utils.get_image_names_in_path(path)), set(["cam1;x_480;y_79;w_53;h_172;1636570203689895900.png",
		                                                       "cam1;x_468;y_78;w_50;h_178;1636570203799268800.png",
                                                               "cam1;x_403;y_78;w_98;h_177;1636570204127382400.png",
		                                                       "cam1;x_444;y_81;w_59;h_174;1636570203908638900.png",
		                                                       "cam1;x_421;y_81;w_77;h_164;1636570204018009000.png",
                                                               "cam1;x_483;y_84;w_70;h_168;1636570203471151300.png",
                                                               "cam1;x_480;y_83;w_65;h_167;1636570203580522800.png"]))


    def test_get_unix_date_from_file_name(self):
        try:
            utils.get_unix_date_from_file_name()
        except TypeError:
            pass
        self.assertEqual(utils.get_unix_date_from_file_name('cam1;x_299;y_198;w_167;h_228;1636565415019736207.png'),
                         '1636565415019736207') 
        self.assertEqual(utils.get_unix_date_from_file_name('cam1;x_301;y_200;w_167;h_222;1836565415025736194.png'),
                         '1836565415025736194')  


    def test_is_time_range_overlaps(self):
        ui_range = Range(time(0, 0), time(23, 59))
        ui_range2 = Range(time(0, 0), time(2, 0))
        range = Range('1636565415019736207', '1836565415025736194')
        try:
            utils.is_time_range_overlaps()
        except TypeError:
            pass
        self.assertEqual(
            utils.is_time_range_overlaps(ui_range, range), True)
        self.assertEqual(
            utils.is_time_range_overlaps(ui_range2, range), False)


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
                         ['cam1;x_303;y_202;w_167;h_150;1636565415019736199.png',
                          'cam1;x_301;y_200;w_167;h_280;1636565415019736200.png',
                          'cam1;x_302;y_201;w_167;h_199;1636565415019736201.png',
                          'cam1;x_299;y_198;w_167;h_218;1636565415019736202.png',
                          'cam1;x_300;y_199;w_167;h_229;1636565415019736206.png'])


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
