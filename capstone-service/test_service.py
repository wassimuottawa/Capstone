import os
import shutil
import unittest

import service


class TestService(unittest.TestCase):

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
        service.ROOT_PATH = 'test root'
        service.ARCHIVE_FOLDER_NAME = 'test archive'
        service.ARCHIVE_PATH = os.path.join(service.ROOT_PATH, service.ARCHIVE_FOLDER_NAME)

    def test_get_folders_by_run(self):
        try:
            service.get_folders_by_run()
        except TypeError:
            pass
        self.assertEqual(service.get_folders_by_run('test run 1'),
                         {'0000000001': ['000000000001'], '0000000002': ['000000000002']})

        self.assertNotEqual(service.get_folders_by_run('test run 1'),
                            {'0000000001': ['000000000001', '000000000004'], '0000000002': ['000000000004']})

    def test_get_image_names(self):
        try:
            service.get_image_names()

        except TypeError:
            pass
        payload = {
            'run': 'test run 1',
            'folder': '0000000001',
            'start': '00:00',
            'end': '23:59'
        }
        payload_2 = {
            'run': 'test run 1',
            'folder': '0000000002',
            'start': '00:00',
            'end': '23:59'
        }
        self.assertEqual(service.get_image_names(payload),
                         {'000000000001': ['cam1;x_306;y_205;w_167;h_235;1636565415019736200.png',
                                           'cam1;x_305;y_204;w_167;h_234;1636565415019736201.png',
                                           'cam1;x_304;y_203;w_167;h_233;1636565415019736202.png',
                                           'cam1;x_303;y_202;w_167;h_232;1636565415019736203.png',
                                           'cam1;x_302;y_201;w_167;h_231;1636565415019736204.png',
                                           'cam1;x_301;y_200;w_167;h_230;1636565415019736205.png',
                                           'cam1;x_300;y_199;w_167;h_229;1636565415019736206.png',
                                           'cam1;x_299;y_198;w_167;h_228;1636565415019736207.png']})
        self.assertEqual(service.get_image_names(payload_2),
                         {'000000000002': ['cam1;x_299;y_198;w_167;h_220;1636565415019736192.png',
                                           'cam1;x_300;y_199;w_167;h_221;1636565415019736193.png',
                                           'cam1;x_301;y_200;w_167;h_222;1636565415019736194.png',
                                           'cam1;x_302;y_201;w_167;h_223;1636565415019736195.png',
                                           'cam1;x_303;y_202;w_167;h_224;1636565415019736196.png',
                                           'cam1;x_304;y_203;w_167;h_225;1636565415019736197.png',
                                           'cam1;x_305;y_204;w_167;h_226;1636565415019736198.png',
                                           'cam1;x_306;y_205;w_167;h_227;1636565415019736199.png']})
        self.assertNotEqual(service.get_image_names(payload),
                            {'000000000002': ['cam1;x_299;y_198;w_167;h_220;1636565415019736192.png',
                                              'cam1;x_300;y_199;w_167;h_221;1636565415019736193.png',
                                              'cam1;x_301;y_200;w_167;h_222;1636565415019736194.png',
                                              'cam1;x_302;y_201;w_167;h_223;1636565415019736195.png',
                                              'cam1;x_303;y_202;w_167;h_224;1636565415019736196.png',
                                              'cam1;x_304;y_203;w_167;h_225;1636565415019736197.png',
                                              'cam1;x_305;y_204;w_167;h_226;1636565415019736198.png',
                                              'cam1;x_306;y_205;w_167;h_227;1636565415019736155.png']})

    def test_get_runs(self):
        try:
            service.get_runs()
        except TypeError:
            pass
        self.assertEqual(service.get_runs(), ['test run 1'])
        self.assertNotEqual(service.get_runs(), ['test run 1', 'test archive'])

    def test_delete_tracklets(self):
        try:
            service.delete_tracklets()
        except TypeError:
            pass
        the_dict = {
            'run': 'test run 1',
            'mapping': {
                "0000000001/000000000001": ['cam1;x_299;y_198;w_167;h_228;1636565415019736207.png',
                                            'cam1;x_300;y_199;w_167;h_229;1636565415019736206.png',
                                            'cam1;x_301;y_200;w_167;h_230;1636565415019736205.png',
                                            'cam1;x_302;y_201;w_167;h_231;1636565415019736204.png',
                                            'cam1;x_303;y_202;w_167;h_232;1636565415019736203.png',
                                            'cam1;x_304;y_203;w_167;h_233;1636565415019736202.png',
                                            'cam1;x_305;y_204;w_167;h_234;1636565415019736201.png',
                                            'cam1;x_306;y_205;w_167;h_235;1636565415019736200.png']
            }
        }
        self.assertEqual(service.delete_tracklets(the_dict), True)

    def test_extract_into_new_folder(self):
        try:
            service.extract_into_new_folder()
        except TypeError:
            pass
        payload = {
            'run': 'test run 1',
            'mapping': {
                '0000000002': ['000000000002']}
        }
        self.assertEqual(service.extract_into_new_folder(payload), '0000000003')

    def test_move_files(self):
        try:
            service.move_files()
        except TypeError:
            pass
        run = 'test run 1'
        file_mapping = {
            '0000000001/000000000001': ['cam1;x_299;y_198;w_167;h_228;1636565415019736207.png',
                                        'cam1;x_300;y_199;w_167;h_229;1636565415019736206.png',
                                        'cam1;x_301;y_200;w_167;h_230;1636565415019736205.png',
                                        'cam1;x_302;y_201;w_167;h_231;1636565415019736204.png',
                                        'cam1;x_303;y_202;w_167;h_232;1636565415019736203.png',
                                        'cam1;x_304;y_203;w_167;h_233;1636565415019736202.png',
                                        'cam1;x_305;y_204;w_167;h_234;1636565415019736201.png',
                                        'cam1;x_306;y_205;w_167;h_235;1636565415019736200.png']
        }
        destination = 'test root/test run 1/0000000001/000000000002'
        self.assertEqual(service.move_files(run, file_mapping, destination), True)

    def tearDown(self):
        service.ROOT_PATH = 'root'
        service.ARCHIVE_FOLDER_NAME = 'archive'
        service.ARCHIVE_PATH = os.path.join(service.ROOT_PATH, service.ARCHIVE_FOLDER_NAME)
        shutil.rmtree('test root')


if __name__ == '__main__':
    unittest.main()
