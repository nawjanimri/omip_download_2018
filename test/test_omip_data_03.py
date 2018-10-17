import os
import unittest
import datetime as dt

import configurador_test
from text_file import TextFile
from formaters import FormaterFecha
#from omip_file_download_02 import OmipFileDownload #, OMIP_PRODUCTS
from omip_data_03 import OmipData #, OMIP_PRODUCTS


#DIR_EJEMPLOS = "..\\tests_omip_files"
DIR_EJEMPLOS = "tests_omip_files"

class OmipData_Test(unittest.TestCase):
	
	def setUp(self):
		
		pass


	def tearDown(self):
		pass


	def test_load_datos_iniciales_from_file(self):

		omip_data = OmipData(get_file_path("omip_data_1.csv"))
		values = omip_data.get_values()
		self.assertEqual(len(values), 14)


	def test_error_si_archivo_datos_iniciales_con_formato_erroneo(self):

		with self.assertRaises(ValueError):
			OmipData(get_file_path("omip_data_formato_erroneo.csv"))


	def test_error_si_archivo_datos_iniciales_no_existe(self):

		with self.assertRaises(FileNotFoundError):
			OmipData("omip_data_no_existente.csv")


	def test_load_datos_iniciales_vacio(self):

		omip_data = OmipData(get_file_path("omip_data_vacio1.csv"))
		values = omip_data.get_values()
		self.assertEqual(len(values), 0)

		omip_data = OmipData(get_file_path("omip_data_vacio2.csv"))
		values = omip_data.get_values()
		self.assertEqual(len(values), 0)


	#INICIO QUITAR DE AQUÍ Y TRASLADAR A OMIP_DB

	def test_get_values_sin_indicar_fecha_muestra_todos_los_values(self):

		omip_data = OmipData(get_file_path("omip_data_1_reducido.csv"))

		values = omip_data.get_values()

		self.assertEqual(len(values), 5)
		#print("values: ", values)
		self.assertEqual(values[dt.datetime(2017, 10, 1), "Q1-18"], 10.44)
		self.assertEqual(values[dt.datetime(2017, 10, 1), "Q2-18"], 20.44)
		self.assertEqual(values[dt.datetime(2017, 10, 2), "Q1-18"], 10.55)
		self.assertEqual(values[dt.datetime(2017, 10, 2), "Q2-18"], 20.55)
		self.assertEqual(values[dt.datetime(2017, 10, 3), "Q1-18"], 11.43)


	def test_raise_error_si_get_values_con_fechas_fin_menor_que_fecha_ini(self):

		ini = dt.datetime(2017, 9, 28) # 28/09/2017
		fin = dt.datetime(2017, 9, 1) # 01/09/2017

		with self.assertRaises(ValueError):
			omip_data = OmipData(get_file_path("omip_data_1.csv"))
			omip_data.get_values(date_ini = ini , date_fin = fin)


	def test_raise_error_si_get_values_con_fecha_superior_a_dia_hoy(self):

		ini = dt.datetime(2017, 10, 2) # 01/10/2017
		manana = dt.datetime.today() + dt.timedelta(days=1)
		with self.assertRaises(ValueError):
			omip_data = OmipData(get_file_path("omip_data_1.csv"))
			omip_data.get_values(ini, manana)


	def test_get_values_si_no_hay_datos(self):

		product_list = ("Q1-18", "Q2-18", "Q3-18", "Q4-18")
		ini = dt.datetime(2017, 10, 2) # 01/10/2017
		fin = dt.datetime(2017, 10, 4) # 03/10/2017

		omip_data = OmipData(get_file_path("omip_data_vacio1.csv"))
		values_db = omip_data.get_values(product_list, ini, fin)
		self.assertEqual(values_db.items(), ()) # No hay datos para el producto solicitado


	def test_get_values_si_no_hay_datos_para_productos_solicitados(self):

		product_list = ("Q4-19")
		ini = dt.datetime(2017, 10, 2) # 01/10/2017
		fin = dt.datetime(2017, 10, 4) # 03/10/2017

		omip_data = OmipData(get_file_path("omip_data_1_reducido.csv"))
		values = omip_data.get_values(product_list, ini, fin)
		self.assertEqual(len(values), 0) # No hay datos para el producto solicitado


#PENDIENTE: VOY POR AQUÍ testeando get_values indicando productos a filtrar


	def test_get_values_entre_dos_fechas(self):

		omip_data = OmipData(get_file_path("omip_data_1_reducido.csv"))

		ini = dt.datetime(2017, 10, 1) # 01/10/2017
		fin = dt.datetime(2017, 10, 2) # 02/10/2017
		values = omip_data.get_values(date_ini = ini , date_fin = fin)

		self.assertEqual(len(values), 4)
		self.assertEqual(values[dt.datetime(2017, 10, 1), "Q1-18"], 10.44)
		self.assertEqual(values[dt.datetime(2017, 10, 1), "Q2-18"], 20.44)
		self.assertEqual(values[dt.datetime(2017, 10, 2), "Q1-18"], 10.55)
		self.assertEqual(values[dt.datetime(2017, 10, 2), "Q2-18"], 20.55)


	def test_get_values_entre_dos_fechas_for_product_list(self):

		products = ("Q1-18", "Q2-18")
		ini = dt.datetime(2017, 10, 1) # 01/10/2017
		fin = dt.datetime(2017, 10, 3) # 03/10/2017

		omip_data = OmipData(get_file_path("omip_data_4_reducido.csv"))
		values = omip_data.get_values(products, ini, fin)
		self.assertEqual(len(values), 6)
		self.assertEqual(values[dt.datetime(2017, 10, 1), "Q1-18"], 10.44)
		self.assertEqual(values[dt.datetime(2017, 10, 1), "Q2-18"], 20.44)
		self.assertEqual(values[dt.datetime(2017, 10, 2), "Q1-18"], 10.55)
		self.assertEqual(values[dt.datetime(2017, 10, 2), "Q2-18"], 20.55)
		self.assertEqual(values[dt.datetime(2017, 10, 3), "Q1-18"], 53.80)
		self.assertEqual(values[dt.datetime(2017, 10, 3), "Q2-18"], 44.05)


#FIN QUITAR DE AQUÍ Y TRASLADAR A OMIP_DB


	def test_update_data_de_product_list(self):

		products = ("Q1-18", "Q2-18") 

		# Initial data
		omip_data = OmipData(get_file_path("omip_data_vacio1.csv"))

		ini = dt.datetime(2017, 10, 4) # 04/10/2017
		fin = dt.datetime.now() 	   # Ahora
		values_antes = omip_data.get_values(products, date_ini = ini , date_fin = fin)

		# Update data
		omip_data.update(products) # Update los productos indicados
		values_despues = omip_data.get_values(date_ini = ini , date_fin = fin)

		# Check data
		self.assertEqual(len(values_despues) > len(values_antes), True)

		# Save data updated
		filepath = get_file_path("omip_data_exportado_1.csv")
		remove_file(filepath)
		omip_data.save_data_to_csv(filepath = filepath)




	def test_update_data(self):

		# Initial data
		omip_data = OmipData(get_file_path("omip_data_vacio1.csv"))

		ini = dt.datetime(2017, 10, 4) # 04/10/2017
		fin = dt.datetime.now() 	   # Ahora
		values_antes = omip_data.get_values(date_ini = ini , date_fin = fin)

		# Update data
		omip_data.update() # Update todos los productos
		values_despues = omip_data.get_values(date_ini = ini , date_fin = fin)

		# Check data
		self.assertEqual(len(values_despues) > len(values_antes), True)

		# Save data updated
		filepath = get_file_path("omip_data_exportado_1.csv")
		remove_file(filepath)
		omip_data.save_data_to_csv(filepath = filepath)


	def test_get_date_range_with_data(self):

		omip_data = OmipData(get_file_path("omip_data_1.csv"))
		fechas = omip_data.get_date_range_with_data()
		self.assertEqual(fechas, (dt.datetime(2017, 10, 1), dt.datetime(2017, 10, 2)))


	def test_get_date_range_with_data_si_no_hay_datos(self):

		omip_data = OmipData(get_file_path("omip_data_vacio1.csv"))
		datos = omip_data.get_date_range_with_data()
		self.assertEqual(datos, (None, None))


#FALTA IMPLEMENTAR TEST PARA "get_dates_with_data" para producto=None


	def test_raise_error_si_get_dates_with_data_para_producto_inexistente(self):

		with self.assertRaises(ValueError):
			omip_data = OmipData(get_file_path("omip_data_1.csv"))
			omip_data.get_dates_with_data("producto que no existe")


	def test_get_dates_with_data_para_producto_sin_datos(self):

		# Initial data
		omip_data = OmipData(get_file_path("omip_data_1.csv"))
		dates_Q4 = omip_data.get_dates_with_data("Q4-19")
		self.assertEqual(dates_Q4, ()) # No hay datos


	def test_get_dates_with_data(self):

		# Initial data
		omip_data = OmipData(get_file_path("omip_data_1.csv"))

		dates_antes = omip_data.get_dates_with_data("Q2-18")
		d1 = dt.datetime(2017, 10, 1) # 01/10/2017
		d2 = dt.datetime(2017, 10, 2) # 02/10/2017
		self.assertEqual(dates_antes, (d1, d2)) #, d3))

		'''
		# Update data
		omip_data.update("Q2-18")

		dates_despues = omip_data.get_dates_with_data("Q2-18")
		self.assertEqual(len(dates_despues)>2, True)

		# Save updated data
		filepath = get_file_path("omip_data_exportado_2.csv")
		remove_file(filepath)
		omip_data.save_data_to_csv(filepath = filepath)
		'''

	def test_save_data_to_csv(self):

		omip_data = OmipData(get_file_path("omip_data_1.csv"))
		
		filepath = get_file_path("omip_data_exportado_1.csv")
		remove_file(filepath)
		omip_data.save_data_to_csv(filepath = filepath)
		
		csv_data = get_file(filepath)
		self.assertEqual(len(csv_data.read_lines()), 15)


	def test_si_get_stats_de_param_no_existente(self):

		bd_file = "omip_data_1.csv" # tiene datos del 01/10/2017 a 02/10/2017
		omip_data = OmipData(get_file_path(bd_file))
		
		self.assertEqual("", omip_data.get_stats("parametro no existente"))
	

	def test_using_omip_to_download_data(self):

		bd_file = "omip_data_1.csv" # tiene datos del 01/10/2017 a 02/10/2017
		omip_data = OmipData(get_file_path(bd_file))
		print_stats("BD cargada desde archivo \"{}\"".format(bd_file), omip_data)

		fecha_fin = omip_data.get_stats("fecha_fin")
		fecha_fin = fecha_fin + dt.timedelta(days=1) # 03/10/2017
		today = dt.datetime.now()
		#omip_data.update(date_ini = fecha_fin,	date_fin = today)
		omip_data.update() # Actualiza todos los productos

		formater_fecha = FormaterFecha(formato = "aaaa-mm-dd")
		bd_file_to_save = "omip_data_" + formater_fecha.formatea(today) + ".csv"
		filepath = get_file_path(bd_file_to_save)
		remove_file(filepath)
		omip_data.save_data_to_csv(filepath = filepath)

		print_stats("BD actualizada desde servidor y datos guardados en archivo \"{}\"".format(
				bd_file_to_save), omip_data)


	# Para descarga de datos ANUALES solicitada por Marcos:
	# ======================================================
	# - Editar "omip_products_01.py" y solicitar sólo productos anuales
	# - Quitar el "No_test...." y dejar como "test_.."
	# - Editar la sección "if __name__ == '__main__':" para que se ejecute sólo este test
	def test_using_omip_to_download_data_de_year(self):

		bd_file = "omip_data_vacio3.csv" # archivo sin datos, sólo cabecera "fecha;producto;valor"
		omip_data = OmipData(get_file_path(bd_file))
		print_stats("BD cargada desde archivo \"{}\"".format(bd_file), omip_data)

		#fecha_fin = omip_data.get_stats()["fecha_fin"]
		#fecha_fin = fecha_fin + dt.timedelta(days=0) # 02/01/2018
		today = dt.datetime.now()
		#omip_data.update(date_ini = fecha_fin,	date_fin = today)
		omip_data.update() # Actualiza todos los productos
		#omip_data.update_multithreading() # Actualiza todos los productos

		formater_fecha = FormaterFecha(formato = "aaaa-mm-dd")
		bd_file_to_save = "omip_data_" + formater_fecha.formatea(today) + ".csv"
		filepath = get_file_path(bd_file_to_save)
		remove_file(filepath)
		omip_data.save_data_to_csv(filepath = filepath)

		print_stats("BD actualizada desde servidor y datos guardados en archivo \"{}\"".format(
				bd_file_to_save), omip_data)


def get_file_path(filename):

	return os.path.join(os.getcwd(), DIR_EJEMPLOS, filename)


def get_file(filepath):

	text_file = TextFile(filepath)

	return text_file


def remove_file(filepath):
	if os.path.exists(filepath):
		os.remove(filepath)


def print_stats(titulo, omip_data):

	print("{}: ".format(titulo))
	print("="*len(titulo))
	print(omip_data)

if __name__ == '__main__':
	
	#unittest.main() # runs any method that starts with the prefix "test", no
					# matter how many classes we create within a given Python module

	
	# Sección para descarga de datos anuales solicitada por MARCOS:
	# =============================================================
	test = OmipData_Test()
	test.setUp()
	#test.test_raise_error_si_check_fechas_con_fecha_superior_a_dia_hoy()
	test.test_using_omip_to_download_data_de_year()
	#test.test_update_data_de_product_list()
	#test.test_si_get_stats_de_param_no_existente()
	#test.test_get_values_si_no_hay_datos()
	#test.test_get_values_entre_dos_fechas()
	#test.test_get_values_entre_dos_fechas_for_product_list()
	#test.test_get_values_for_products()
	'''
	
	test.test_error_si_archivo_datos_iniciales_con_formato_erroneo()
	test.test_load_datos_iniciales_vacio()
	test.test_error_si_archivo_datos_iniciales_no_existe()
	test.test_get_values_sin_indicar_fecha_muestra_todos_los_values()
	test.test_raise_error_si_get_values_con_fechas_fin_menor_que_fecha_ini()
	test.test_cumple_get_value_date_range()
	test.test_get_values_entre_dos_fechas()
	test.test_update_data()
	test.test_get_dates_with_data()
	test.test_get_values_for_products()
	test.test_save_data_to_csv()
	test.test_using_omip_to_download_data()
	'''
	