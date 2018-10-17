# -*- coding: cp1252 -*
import datetime as dt
import os
import unittest

import configurador_test
from omip_file_writer_02 import OmipStoredDataWriter
from omip_file_reader_05 import OmipStoredDataReader
from omip_db_02 import OmipDB

#DIR_EJEMPLOS = "..\\tests_omip_files"
DIR_EJEMPLOS = "tests_omip_files"

class OmipStoredDataWriter_Test(unittest.TestCase):
	
	def setUp(self):
		
		pass


	def tearDown(self):
		pass


	def test_error_si_archivo_datos_ya_existe(self):

		filepath = get_file_path("omip_data_ya_existente.csv")

		with self.assertRaises(FileExistsError):
			writer = OmipStoredDataWriter()
			writer.write_data(OmipDB(), filepath)


	def test_error_si_guarda_datos_con_formato_erroneo(self):

		filepath = get_file_path("cualquier_archivo.csv")

		with self.assertRaises(TypeError):
			writer = OmipStoredDataWriter()
			writer.write_data("datos_que_no_son_OmipDb", filepath)


	def test_guarda_datos_vacios_en_archivo_no_da_error(self):

		filepath = get_file_path("omip_data_vacio3.csv")

		if os.path.isfile(filepath):
			os.remove(filepath)
		writer = OmipStoredDataWriter()
		db = OmipDB() 
		writer.write_data(db, filepath)


	def test_guarda_datos_en_archivo(self):

		filepath = get_file_path("omip_data_3_lineas.csv")
		reader = OmipStoredDataReader()
		data = reader.read_data(filepath)
		self.assertEqual(len(data), 3)

		# Leo lo que hay inicialmente
		print("data ", data.items())
		self.assertEqual(data[dt.datetime(2017,10,1),"Q2-18"], 10.44)
		self.assertEqual(data[dt.datetime(2017,10,2),"Q3-19"], 70.55)


		# Modifico los datos y guardo de nuevo
		data[dt.datetime(2017,10,1),"Q2-18"] = 10
		data[dt.datetime(2017,10,2),"Q3-19"] = 20

		print("data ", data.items())

		filepath_2 = get_file_path("omip_data_3_lineas_modificado.csv")
		if os.path.isfile(filepath_2):
			os.remove(filepath_2)
		writer = OmipStoredDataWriter()
		writer.write_data(data, filepath_2)

		# Y compruebo que se ha actulizado bien
		reader = OmipStoredDataReader()
		data = reader.read_data(filepath_2)
		self.assertEqual(len(data), 3)
		print("data ", data.items())
		self.assertEqual(data[dt.datetime(2017,10,1),"Q2-18"], 10)
		self.assertEqual(data[dt.datetime(2017,10,2),"Q3-19"], 20)

		

def get_file_path(filename):

	return os.path.join(os.getcwd(), DIR_EJEMPLOS, filename)


if __name__ == '__main__':
	unittest.main() # runs any method that starts with the prefix "test", no
					# matter how many classes we create within a given Python module

	'''
	test = OmipDownload_Test()
	test.setUp()
	test.test_raise_error_si_download_raw_file_con_fechas_futuras()
	test.test_raise_error_si_download_raw_file_con_fechas_fin_menor_que_fecha_ini()
	test.test_download_raw_file()
	'''
	
	'''
	test = OmipData_Test()
	test.setUp()
	test.test_error_si_archivo_datos_iniciales_con_formato_erroneo()
	test.test_load_datos_iniciales_vacio()
	test.test_error_si_archivo_datos_iniciales_no_existe()
	test.test_load_datos_iniciales_from_file()
	test.test_get_values_sin_indicar_fecha_muestra_todos_los_values()
	test.test_raise_error_si_get_values_con_fechas_fin_menor_que_fecha_ini()
	test.test_cumple_get_value_date_range()
	test.test_get_values_entre_dos_fechas()
	test.test_update_data()
	#test.test_get_date_range_with_data()
	'''
	