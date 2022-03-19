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

        json_text_1 = '{\n  "min_detection_time": "1636570201361845700",\n  "max_detection_time": "1636570208080372300",\n  "num_detections": 58\n}'
        json_text_2 = '{\n  "min_detection_time": "1636570499087158600",\n  "max_detection_time": "1636570509664929900",\n  "num_detections": 82\n}'

        with open(os.path.join(test_root_path, "test run 1", "0000000001", "000000000001", "000000000001.json"), 'w') as json_file:
            json_file.write(json_text_1)
        with open(os.path.join(test_root_path, "test run 1", "0000000002", "000000000002", "000000000002.json"), 'w') as json_file:
            json_file.write(json_text_2)

        service.ROOT_PATH = 'test root'
        service.ARCHIVE_FOLDER_NAME = 'test archive'
        service.ARCHIVE_PATH = os.path.join(service.ROOT_PATH, service.ARCHIVE_FOLDER_NAME)


    def test_get_runs(self):
        try:
            service.get_runs()
        except TypeError:
            pass
        self.assertEqual(service.get_runs(), ['test run 1'])
        self.assertNotEqual(service.get_runs(), ['test run 1', 'test archive'])


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

        self.assertEqual(service.get_image_names(payload),
                         {'000000000001': ["cam1;x_483;y_84;w_70;h_168;1636570203471151300.png",
	                                       "cam1;x_480;y_83;w_65;h_167;1636570203580522800.png",
		                                   "cam1;x_480;y_79;w_53;h_172;1636570203689895900.png",
		                                   "cam1;x_468;y_78;w_50;h_178;1636570203799268800.png",
		                                   "cam1;x_444;y_81;w_59;h_174;1636570203908638900.png",
		                                   "cam1;x_421;y_81;w_77;h_164;1636570204018009000.png",
		                                   "cam1;x_403;y_78;w_98;h_177;1636570204127382400.png"]})

        self.assertNotEqual(service.get_image_names(payload),
                            {'000000000002': ["cam1;x_195;y_65;w_58;h_163;1636570206424179900.png",
		                                      "cam1;x_188;y_65;w_56;h_148;1636570206533550500.png",
		                                      "cam1;x_182;y_64;w_60;h_143;1636570206642920400.png",
		                                      "cam1;x_170;y_65;w_61;h_144;1636570206877291100.png",
		                                      "cam1;x_171;y_63;w_57;h_142;1636570206986659800.png",
		                                      "cam1;x_165;y_64;w_56;h_133;1636570207096032500.png",
		                                      "cam1;x_165;y_64;w_56;h_134;1636570207205401700.png"]})


    def test_extract_into_new_folder(self):
        try:
            service.extract_into_new_folder()
        except TypeError:
            pass
        payload = {
            'run': 'test run 1',
            'mapping': {
                '0000000001': ['000000000001'],
                '0000000002': ['000000000002']
            }
        }
        self.assertEqual(service.extract_into_new_folder(payload), '0000000001')
    

    def test_move_files(self):
        try:
            service.__move_files()
        except TypeError:
            pass
        run = 'test run 1'
        file_mapping = {
            "0000000001": ["000000000001"]
        }
        destination = 'test root/test run 1/0000000002'
        self.assertEqual(service.__move_files(run, file_mapping, destination), True)


    def test_delete_tracklets(self):
        try:
            service.delete_tracklets()
        except TypeError:
            pass
        the_dict = {
            'run': 'test run 1',
            'mapping': {
                "0000000002": ["000000000002"]
            }
        }
        self.assertEqual(service.delete_tracklets(the_dict), True)


    def tearDown(self):
        service.ROOT_PATH = 'root'
        service.ARCHIVE_FOLDER_NAME = 'archive'
        service.ARCHIVE_PATH = os.path.join(service.ROOT_PATH, service.ARCHIVE_FOLDER_NAME)
        shutil.rmtree('test root')


if __name__ == '__main__':
    unittest.main()
