# -*- coding: cp1252 -*
import os
import unittest

import configurador_test
from text_file import TextFile
from omip_file_download_02 import OmipFileDownload #, OMIP_PRODUCTS


#DIR_EJEMPLOS = "..\\tests_omip_files"
DIR_EJEMPLOS = "tests_omip_files"


class OmipDownload_Test(unittest.TestCase):
	
	def setUp(self):
		
		pass

	def tearDown(self):
		pass


	def test_error_si_archivo_archivo_ya_existe(self):

		product = "Q2-18"

		with self.assertRaises(FileExistsError):
			omip_down = OmipFileDownload()
			omip_down.download_product_raw_file(product, "omip_data_ya_existente.csv")

	'''		
	def test_raise_error_si_download_raw_file_con_producto_inexistente(self):

		omip_down = OmipFileDownload("path de prueba")

		with self.assertRaises(ValueError):
			omip_down.download_raw_file("producto que no existe")
	'''

	def test_raise_error_si_download_raw_file_en_archivo_inexistente(self):

		filepath  = get_file_path("omip_raw_file_ya_existe.html")
		omip_down = OmipFileDownload()

		with self.assertRaises(FileExistsError):
			omip_down.download_product_raw_file("Q2-18", filepath)


	def test_download_raw_file(self):

		# Eliminar el archivo, si es que existe previamente
		filepath = get_file_path("omip_raw_data_1.csv")
		remove_file(filepath)

		# Descargar el archivo raw
		omip_down = OmipFileDownload()
		omip_down.download_product_raw_file("Q2-18", filepath)

		# Comprobar el contenido descargado
		text_file = get_text_file(filepath)
		lineas = text_file.read_lines()
		self.assertEqual(len(lineas), 1)
		self.assertGreater(len(lineas[0]), 500)
		self.assertTrue("[1467763200000,39.41]" in lineas[0], True)
		self.assertTrue("[1514941200000,48.13]" in lineas[0], True)


def get_file_path(filename):

	return os.path.join(os.getcwd(), DIR_EJEMPLOS, filename)


def get_text_file(filepath):

	text_file = TextFile(filepath)

	return text_file


def remove_file(filepath):
	if os.path.exists(filepath):
		os.remove(filepath)


if __name__ == '__main__':

	'''
	import nose
	
	#import os
	import sys
	sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
	config = nose.config.Config(verbosity=3, stopOnError=False, argv=["--with-coverage"])
	result = nose.run(config=config)

	#nose.main("with coverage")
	'''

	unittest.main() # runs any method that starts with the prefix "test", no
					# matter how many classes we create within a given Python module
	'''
	test = OmipDownload_Test()
	test.setUp()
	test.test_raise_error_si_download_raw_file_con_producto_inexistente()
	test.test_raise_error_si_download_raw_file_en_archivo_inexistente()
	test.test_raise_error_si_download_raw_file_con_fechas_futuras()
	test.test_raise_error_si_download_raw_file_con_fechas_fin_menor_que_fecha_ini()
	test.test_download_raw_file()
	'''
	