import datetime as dt
import abc

import configurador_test
from time_util import epoch_to_dt
from parsers import ParserFecha, ParserFloat
from text_file import TextFile
from splitters import TextSplitter
from csv_reader import LineFilter, LineParser, CsvFilter
from omip_db_02 import OmipDB

#STR_INI = "price\",\"data\":[" # Q
STR_INI = "},\"data\":["	# YR
#STR_INI = ",\"data\":["	# YR
STR_END = "]}]}'></div>"


class OmipFileReader():
	''' Clase base para la lectura de ficheros de OMIP'''
	
	def __init__(self):

		pass
		#self._csv_path = csv_path # ruta del fichero csv con los datos a leer
		#self._num_items_por_linea_csv = 0


	def read_data(self, csv_path):

		data = self._load_data_from_file(csv_path) # csv_path: ruta del fichero csv con los datos a leer
		#print("data loaded: ", data)
		return data


	def _load_data_from_file(self, csv_path):
		''' lee el archivo csv y devuelve los datos en forma de base de datos OmipDB'''
		db = OmipDB()

		for item in self._get_items_from_csv_file(csv_path):
			(fecha, producto, valor) = item
			db.save_item(fecha, producto, valor)

		return db


	@abc.abstractmethod
	def _get_items_from_csv_file(self, csv_path):

		raise NotImplementedError("Se debe implementar este método en la clase derivada")
	

class OmipStoredDataReader(OmipFileReader):

	def __init__(self):

		super().__init__()
		self._num_items_por_linea_csv = 3 #[dia; producto; value]


	def _get_items_from_csv_file(self, csv_path):

		for line in self._get_lines_from_csv_data_yield(csv_path):
			#print("linea leida: ", line)
			self._check_formato_linea(line)
			yield self._process_line(line) #(fecha, producto, valor)


	def _get_lines_from_csv_data_yield(self, csv_path):

		csv_file 	= TextFile(csv_path)
		
		splitter    = TextSplitter(";", trim_trozos = True)
		
		line_filter = LineFilter(splitter = splitter)
		line_parser = LineParser()

		parser_fecha = ParserFecha("dd/mm/aaaa")
		parser_float = ParserFloat()
		line_parser.add_parser_for_cols(parser_fecha, 0)
		line_parser.add_parser_for_cols(parser_float, 2)

		#	filtro = CsvFilter(skip_lines = (0), line_filter = line_filter, line_parser = line_parser)
			
		filtro = CsvFilter(skip_lines = (0), line_filter = line_filter, line_parser = line_parser)

		return filtro.get_filtered_lines_yield(csv_file)

	
	def _check_formato_linea(self, linea):
		#print("linea desde _check_formato: ", linea)
		#def raise_error():
		
		# formato correcto de línea: [dia; producto; value]
		#if not linea or type(linea) is not list:
		#	raise_error()
		if len(linea) != self._num_items_por_linea_csv:
			#raise_error()
			raise ValueError("La línea \"{}\" no tiene un formato de liquidación correcto".format(linea))


	def _process_line(self, line):

		fecha 	 = line[0]
		producto = line[1]
		valor 	 = line[2]

		return (fecha, producto, valor)


class OmipRawDataReader(OmipFileReader):

	def __init__(self):

		super().__init__()
		#self._producto = producto


	def read_data(self, producto, csv_path):

		self._producto = producto
		data = super().read_data(csv_path) # csv_path: ruta del fichero csv con los datos a leer
		#print("data loaded: ", data)
		return data
	

	def _get_items_from_csv_file(self, csv_path):
		''' extrae el texto en formato raw del archivo csv, extrae los valores del 
				texto raw, y procesa los items del mismo.'''
		texto_raw = self._get_texto_raw(csv_path)
		self._check_texto_cumple_formato(texto_raw)
		texto_valores = self._get_texto_valores(texto_raw)
		
		if texto_valores:
			#from text_extractor import extrae_muestra_texto
			#muestra = extrae_muestra_texto(texto_valores, ini=40, fin=20)
			#print("texto valores: \"{}\", con len: {}".format(muestra, len(texto_valores)))
			for item in self._process_items(texto_valores):
				yield item
		
		# Si no hay texto con valores (Ej: archivo vacío), no se devuelve nada


	def _get_texto_raw(self, csv_path):
		'''extrae el texto en bruto con los valores, del archivo raw'''
		#https://stackoverflow.com/questions/8369219/how-do-i-read-a-text-file-into-a-string-variable-in-python
		texto = ""
		with open(csv_path, "r") as f:
			texto = f.read()	 # contenido completo del archivo
			return texto.strip() # elimina espacios adicionales que hubiera delante y detrás del texto


	def _check_texto_cumple_formato(self, texto_raw):
		'''comprueba si el texto raw tiene el formato correcto para contener los valores
			que buscamos extraer. Básicamente si el texto se inicia y finaliza con unos 
			caracteres determinados'''
		if len(texto_raw) > 0:
			# El texto raw debe contener los trozos STR_INI y terminar por STR_END
			if (STR_INI in texto_raw) and (texto_raw.endswith(STR_END)):  #YR
				pass
			else:
				raise ValueError("El archivo no tiene el formato correcto: ", texto_raw)
		# Si el texto está vacío, se considera válido


	def _get_texto_valores(self, texto_raw):	
		'''extrae del texto completo raw el trozo de texto que contiene los valores 
		omip que se buscan'''
		if len(texto_raw) == 0:
			#print("texto raw con longitud cero")
			return None

		pos_ini = texto_raw.index(STR_INI) + len(STR_INI)
		pos_end = len(STR_END)
		texto_valores = texto_raw[pos_ini: -pos_end]

		return texto_valores # cadena de valores extraidos del archivo en formato [epoch time, valor]. 
							 #	Ejemplo: "[1463097600000,40.02],[1463356800000,40.32],[1463443200000,40.36],..."

	def _process_items(self, texto_valores):
		'''extrae los items de cotización que contiene el texto.
			Cada item está en formato [epoch time, valor] pero se devuelven como
			(fecha, producto, valor'''

		try:
			# Se convierte a número los valores del texto "[1463097600000,40.02],[1463356800000,40.32],...""
			import ast
			valores = ast.literal_eval(texto_valores) # tupla con valores ([1463097600000,40.02],[1463356800000,40.32],...)
			#print("valores: ", valores)

			for valor in valores:
				[epoch, cotizacion] = valor
				fecha = self._epoch_to_dt(epoch)
				yield (fecha, self._producto, cotizacion)
		except ValueError as ex:
			muestra_valores = texto_valores[:min(20, len(texto_valores))]
			raise ValueError("Error al extraer los items [epoch, valor] "
					"del texto raw: {}".format(muestra_valores), ex.args)


	def _epoch_to_dt(self, epoch):
		'''convierte una fecha desde formato epoch a datetime'''
		epoch_seconds = epoch/1000
		fecha = epoch_to_dt(epoch_seconds)
		# me quedo sólo con la fecha, no quiero las horas y minutos:
		fecha_sin_horas = dt.datetime(fecha.year, fecha.month, fecha.day)
		#print("feha epoch: ", fecha_sin_horas)

		return fecha_sin_horas


