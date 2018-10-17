import os
import datetime as dt

#import configurador

#from formaters.formater_float_01 import FormaterFloat
from formaters import FormaterFecha
from omip_file_download_02 import OmipFileDownload
from omip_file_reader_05 import OmipStoredDataReader, OmipRawDataReader
from omip_file_writer_02 import OmipStoredDataWriter
#from omip_db_02 import OmipDB
from omip_products_01 import OmipProductos
from omip_stats_01 import OmipStats

# URL: http://kazuar.github.io/scraping-tutorial/
# URL: https://stackoverflow.com/questions/15646813/file-download-via-post-form
# URL: https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
# URL: https://stackoverflow.com/questions/35747033/how-to-download-files-in-python-with-post-request

DIR_EJEMPLOS = "" #"..\\tests_omip_files"

#OMIP_PRODUCTS = ("Q1-18", "Q2-18", "Q3-18", "Q4-18", "Q1-19", "Q2-19", "Q3-19", "Q4-19")


class OmipData():

	def __init__(self, csv_path):
		'''csv_path: ruta del archivo csv con los datos Omip
		'''
		self._stats = OmipStats()
		self._stats.reset_stats()
		self._data = self._load_data_from_stored_file(csv_path)
		#print("data loaded: ", self._data)
		#print("lineas loaded from stored file: ", len(self._data.items()))
		self._stats.update(self._data)


	def _load_data_from_stored_file(self, csv_path):

		reader = OmipStoredDataReader()
		data = reader.read_data(csv_path)
		return data


	def update_OLD(self, lista_productos=""):
		'''Actualiza los datos del producto indicado.
		Si no se indica un producto, actualiza los datos de todos los productos
		de la base de datos de productos.'''
		
		productos = None

		if lista_productos:
			productos = lista_productos
			#self._update(producto)
		else:
			productos = OmipProductos.get_productos()


		#PENDIENTE, meter aquí multithreading:
		for prod in productos:
			
			#AQUÍ IMPLEMENTAR THREADING
			print("producto: ", prod)
			self._update(prod)

	# multithreading:
	def update(self, lista_productos=""):
		'''Actualiza los datos del producto indicado.
		Si no se indica un producto, actualiza los datos de todos los productos
		de la base de datos de productos.'''
		import queue
		import threading

		productos = None

		if lista_productos:
			productos = lista_productos
			#self._update(producto)
		else:
			productos = OmipProductos.get_productos()

		# Multithreading:
		# ------------------
		#num_worker_threads = 4
		num_worker_threads = min(len(productos), 4)
			
		def worker():
			while True:
				item = q.get()
				if item is None:
					break
				#do_work(item)
				print("producto: ", item)
				self._update(item)
				q.task_done()

		q = queue.Queue()
		threads = []
		for i in range(num_worker_threads):
			t = threading.Thread(target=worker)
			t.start()
			threads.append(t)

		for item in productos:
			q.put(item)

		# block until all tasks are done
		q.join()

		# stop workers
		for i in range(num_worker_threads):
			q.put(None)
		for t in threads:
			t.join()

		# END Multithreading:
		# ------------------


	def _update(self, producto):

		new_data = self._load_raw_data_for_producto(producto)
		self._data.update(new_data)
		data_list = sorted(list(new_data.items())) # hace el list con los items completos del dict	
		
		omip_ini = data_list[0]		# ((20/11/2017, Q2-18), 40.06)
		omip_fin = data_list[-1]	# ((23/11/2017, Q2-18), 47.23)
		fecha_ini = omip_ini[0]  	# 20/11/2017
		fecha_fin = omip_fin[0]  	# 23/11/2017
		self._stats.update(self._data,
				fecha_last_update_from_server = dt.datetime.now(),
				fecha_ini_data_last_update_from_server = fecha_ini, 
				fecha_fin_data_last_update_from_server = fecha_fin,
				num_registros_last_update_from_server = len(new_data))


	def _load_raw_data_for_producto(self, producto):

		raw_path = self._download_omip_file(producto)
		print("csv_path: ", raw_path)

		reader = OmipRawDataReader()
		data = reader.read_data(producto, raw_path) # devuelve un OmipDB
		self._remove_file(raw_path)
		
		return data


	def _download_omip_file(self, producto):

		temp_path = self._get_temp_path_to_download_file(producto)
		self._remove_file(temp_path)
		omip_down = OmipFileDownload()
		omip_down.download_product_raw_file(producto, temp_path)
		return temp_path


	def _get_temp_path_to_download_file(self, producto):

		fecha_download = dt.datetime.now()
		formater = FormaterFecha(formato = "dd-mm-aaaa")
		filename = "omip_temp_{}_{}.csv".format(producto, formater.formatea(fecha_download))
		filepath = os.path.join(os.getcwd(), DIR_EJEMPLOS, filename)
		return filepath


	def _remove_file(self, filepath):
		
		if os.path.exists(filepath):
			os.remove(filepath)


	def get_values(self, product_list=None, date_ini = None, date_fin = None):

		#self._check_fechas(date_ini, date_fin)
		#print("tipo de data: ", type(self._data))
		return self._data.get_items(product_list, date_ini, date_fin)

	
	def get_dates_with_data(self, producto=None):

		dias_with_data = []

		if producto:
			#self._check_producto_existe(producto)
			OmipProductos.check_existe_producto(producto)

			for (fecha, producto_name, _) in self._data.items(): 
				#print("fecha y product name", (fecha, producto_name))
				if producto_name == producto:
					dias_with_data.append(fecha)

			#print("keys :", self._data.keys())
			#print("productos leidos: ", len(dias_with_data))
		else:
			dias_with_data = [fecha for (fecha, _, _) in self._data.items()]

		if dias_with_data:
			dias_with_data.sort()
			return tuple(dias_with_data)
		else:
			return () # Si no hay datos para ese producto


	def get_date_range_with_data(self):

		if not self._data:
			return (None, None)

		data_keys = sorted(list(self._data.items())) # sólo hace el list con los keys() del dict
		(omip_ini, omip_fin) = (data_keys[0], data_keys[-1])
		(fecha_ini, fecha_fin) = (omip_ini[0], omip_fin[0])
		return (fecha_ini, fecha_fin)


	def save_data_to_csv(self, filepath):

		#self._check_file_no_existe_todavia(filepath)
		writer = OmipStoredDataWriter()
		writer.write_data(self._data, filepath)


	def get_stats(self, param):

		return self._stats.get_stats(param)


	def __repr__(self):

		import os
		s = []
		for key, value in self._stats.get_items():
			s.append(key + ": " + str(value))

		return os.linesep.join(s)





	





