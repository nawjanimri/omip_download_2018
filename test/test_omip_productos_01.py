# -*- coding: cp1252 -*
import unittest

import configurador_test
from omip_products_01 import OmipProductos

#DIR_EJEMPLOS = "..\\tests_omip_files"
DIR_EJEMPLOS = "tests_omip_files"

class OmipProductos_Test(unittest.TestCase):
	
	def setUp(self):
		
		pass


	def tearDown(self):
		
		pass


	def test_error_si_producto_no_existe(self):

		with self.assertRaises(ValueError):
			OmipProductos.check_existe_producto("producto que no existe")


	def test_get_URL_for_producto_si_producto_no_existe_da_error(self):

		with self.assertRaises(ValueError):
			OmipProductos.get_URL_for_producto("producto que no existe")


	def test_get_URL_for_producto(self):

		#url_ok = "https://www.omip.pt/en/javali/get_full_chart/FTBQ2-18/0/0/0/1"
		url_ok = "https://www.omip.pt/en/javali/get_full_chart/FTBQ2-18/0/1"
		url = OmipProductos.get_URL_for_producto("Q2-18")
		self.assertEqual(url, url_ok)


	def test_get_productos(self):

		productos = OmipProductos.get_productos()
		self.assertEqual(productos, ("Q1-18", "Q2-18", "Q3-18", "Q4-18", "Q1-19", 
			"Q2-19", "Q3-19", "Q4-19"))




if __name__ == '__main__':
	unittest.main() # runs any method that starts with the prefix "test", no
					# matter how many classes we create within a given Python module

	