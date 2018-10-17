# -*- coding: cp1252 -*
#import pdb
import datetime as dt
import os
import unittest

import configurador_test
from omip_file_reader_05 import OmipFileReader, OmipStoredDataReader, OmipRawDataReader #, OMIP_PRODUCTS

#DIR_EJEMPLOS = "..\\tests_omip_files"
DIR_EJEMPLOS = "tests_omip_files"

class OmipFileReader_Test(unittest.TestCase):

	def setUp(self):
		
		pass


	def tearDown(self):
		pass


	def test_error_si_no_implemento_bien_clase_derivada(self):

		class Clase_test(OmipFileReader):
			def __init__(self):
				pass

		with self.assertRaises(NotImplementedError):
			mi_clase = Clase_test()
			mi_clase.read_data("omip_data_vacio1.csv")



class OmipStoredDataReader_Test(unittest.TestCase):
	
	def setUp(self):
		
		pass


	def tearDown(self):
		pass


	def test_error_si_archivo_con_formato_erroneo(self):
		#pdb.set_trace()
		with self.assertRaises(ValueError):
			reader = OmipStoredDataReader()
			reader.read_data(get_file_path("omip_data_formato_erroneo.csv"))

		with self.assertRaises(ValueError):
			reader = OmipStoredDataReader()
			reader.read_data(get_file_path("omip_data_formato_erroneo_muchos_elementos.csv"))


	def test_error_si_archivo_datos_iniciales_no_existe(self):

		with self.assertRaises(FileNotFoundError):
			reader = OmipStoredDataReader()
			reader.read_data("omip_data_no_existente.csv")


	def test_read_archivo_con_datos_vacio(self):

		reader = OmipStoredDataReader()
		data = reader.read_data(get_file_path("omip_data_vacio1.csv"))
		self.assertEqual(len(data), 0)

		reader = OmipStoredDataReader()
		data = reader.read_data(get_file_path("omip_data_vacio2.csv"))
		self.assertEqual(len(data), 0)


	def test_read_archivo_con_datos(self):

		reader = OmipStoredDataReader()
		data = reader.read_data(get_file_path("omip_data_2_lineas.csv"))
		self.assertEqual(len(data), 2)

		print("data ", data)
		self.assertEqual(data[dt.datetime(2017,10,1),"Q2-18"], 10.44)
		self.assertEqual(data[dt.datetime(2017,10,2),"Q3-19"], 70.55)	



class OmipRawDataReader_Test(unittest.TestCase):
	
	def setUp(self):
		
		pass


	def tearDown(self):
		pass
		

	def test_error_si_archivo_con_formato_erroneo(self):

		with self.assertRaises(ValueError):
			reader = OmipRawDataReader()
			reader.read_data("Q2-18", get_file_path("omip_raw_data_formato_erroneo.htm"))


	def test_error_si_archivo_datos_iniciales_no_existe(self):

		with self.assertRaises(FileNotFoundError):
			reader = OmipRawDataReader()
			reader.read_data("Q2-18", "omip_data_no_existente.htm")


	def test_archivo_con_datos_vacio(self):

		reader = OmipRawDataReader()
		data = reader.read_data("Q2-18", get_file_path("omip_raw_vacio1.htm"))
		self.assertEqual(len(data), 0)

		reader = OmipRawDataReader()
		raw_data = reader._get_texto_raw(get_file_path("omip_raw_vacio2.htm"))
		self.assertEqual(raw_data.endswith("\n"), False)
		data = reader.read_data("Q2-18", get_file_path("omip_raw_vacio2.htm"))
		self.assertEqual(len(data), 0)


	def test_linea_cumple_filtro(self):

		reader = OmipRawDataReader()

		texto_mal = "asdfasd"
		with self.assertRaises(ValueError):
			reader._check_texto_cumple_formato(texto_mal)

		# textos que cumplen formato no lanzan excepción
		reader._check_texto_cumple_formato("")

		#texto_bien_1 = "price\",\"data\":[]}]}'></div>"
		#texto_bien_1 = ",\"data\":[]}]}'></div>"
		texto_bien_1 = "},\"data\":[]}]}'></div>"
		reader._check_texto_cumple_formato(texto_bien_1)

		#"price\",\"data\":["  "]}]}'></div>"
	
		#texto_bien_2 = "price\",\"data\":[aqui van los datos]}]}'></div>"
		texto_bien_2 = "},\"data\":[aqui van los datos]}]}'></div>"
		reader._check_texto_cumple_formato(texto_bien_2)

		#texto_ok_pero_sin_datos = "price\",\"data\":[hhh]}]}'></div>"
		texto_ok_pero_sin_datos = "},\"data\":[hhh]}]}'></div>"
		reader._check_texto_cumple_formato(texto_ok_pero_sin_datos)


	def test_get_texto_valores(self):

		reader = OmipRawDataReader()

		texto_raw_1 = reader._get_texto_raw(get_file_path("omip_raw_vacio1.htm"))
		self.assertEqual(texto_raw_1, "")

		texto_raw_2 = reader._get_texto_raw(get_file_path("omip_raw_data_2_datos.htm"))
		texto_valores = reader._get_texto_valores(texto_raw_2)
		self.assertEqual(texto_valores, "[1467331200000,39.37],[1467590400000,39.53]")

		texto_raw_3 = reader._get_texto_raw(get_file_path("omip_raw_data_completo.htm"))
		self.assertEqual(len(texto_raw_3) > 2000, True)
		#print("texto_raw_3, ", texto_raw_3)

		print("texto_valores_3, ", len(reader._get_texto_valores(texto_raw_3)))
		print("texto_valores_4, ", len(reader._get_texto_valores(texto_raw_2)))
		print("texto_valores_4", reader._get_texto_valores(texto_raw_2))


	def test_process_items_con_valores_parseables(self):

		import datetime as dt
		reader = OmipRawDataReader()
		reader._producto = "Q2-18"

		texto = "[1463097600000, 40.02], [1463356800000, 40.32]"
		items_ok = [(dt.datetime(2016, 5, 13, 0, 0), reader._producto, 40.02), 
					(dt.datetime(2016, 5, 16, 0, 0), reader._producto, 40.32)]
		i = 0
		for item in reader._process_items(texto):
			self.assertEqual(item, items_ok[i])
			i += 1


	def test_error_al_process_items_con_valores_no_parseables(self):

		reader = OmipRawDataReader()
		reader._producto = "Q2-18"

		texto = "[1463097600000, hola], [1463356800000, hola]"
		
		with self.assertRaises(ValueError):
			for item in reader._process_items(texto):
				print(item)


	def test_read_data_de_archivo(self):

		reader = OmipRawDataReader()
		data = reader.read_data("Q2-18", get_file_path("omip_raw_data_2_datos.htm"))
		self.assertEqual(len(data), 2)
		self.assertEqual(data.get_item(dt.datetime(2016,7,1),"Q2-18"), 39.37)
		self.assertEqual(data.get_item(dt.datetime(2016,7,4),"Q2-18"), 39.53)
		print("len data: ", len(data))
		print("data[0]", data.items()[0])
		print("data[-1]", data.items()[-1])

		reader = OmipRawDataReader()
		data = reader.read_data("Q2-18", get_file_path("omip_raw_data_muchos_datos.htm"))
		self.assertEqual(len(data), 419)
		print("len data: ", len(data))
		self.assertEqual(data.items()[0], (dt.datetime(2016, 5, 13, 0, 0), "Q2-18", 40.02))
		self.assertEqual(data.items()[-1], (dt.datetime(2017, 12, 28, 0, 0), 'Q2-18', 54.22))
		print("data[0]", data.items()[0])
		print("data[-1]", data.items()[-1])

		reader = OmipRawDataReader()
		raw_file = r"C:\JMAlvarez\Apuntes\z_Programacion\Python\Proyectos_Nuevo\omip_downloads_2018\test\tests_omip_files\omip_raw_data_muchos_datos.htm"
		data = reader.read_data("Q2-18", raw_file)
		self.assertEqual(len(data), 419)
		print("len data: ", len(data))
		print("data[0] ", data.items()[0])
		print("data[-1] ", data.items()[-1])
		print("item[-1]", data.items()[-1])


def get_file_path(filename):

	return os.path.join(os.getcwd(), DIR_EJEMPLOS, filename)


if __name__ == '__main__':
	
	unittest.main() # runs any method that starts with the prefix "test", no
					# matter how many classes we create within a given Python module

	
	'''
	test0 = OmipFileReader_Test()
	test0.setUp()
	test0.test_error_si_no_implemento_bien_clase_derivada()

	
	test1 = OmipStoredDataReader_Test()
	test1.setUp()
	test1.test_read_archivo_con_datos_vacio()
	
	
	test2 = OmipRawDataReader_Test()
	test2.setUp()
	test2.test_archivo_con_datos_vacio()
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

	