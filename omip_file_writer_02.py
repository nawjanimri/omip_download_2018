import os
import csv

from formaters import FormaterFloat
from formaters import FormaterFecha

from omip_db_02 import OmipDB

class OmipStoredDataWriter():

	def __init__(self):

		#self._file_to_save_path = csv_path
		self._formaters = {}
		self._formaters["float"] = FormaterFloat(formato = "#.##", char_decimal = ".")
		self._formaters["fecha"] = FormaterFecha(formato = "dd/mm/aaaa")


	def write_data(self, omip_db, csv_path):

		self._check_omip_db_correcta(omip_db)
		self._check_file_no_existe_todavia(csv_path)

		sep = ";"
		with open(csv_path, 'w', newline = "") as f:
			csv_writer = csv.writer(f, delimiter=sep)
			self._write_titulo(csv_writer)
			self._write_items_de_tabla(csv_writer, omip_db)


	def _check_omip_db_correcta(self, omip_db):

		if type(omip_db) is not OmipDB:
			raise TypeError("Los datos que intenga guardar no son de tipo OmipDB")


	def _check_file_no_existe_todavia(self, filepath):

		if os.path.isfile(filepath):
			filename = os.path.basename(filepath)
			raise FileExistsError("El archivo \"{}\" ya existe y no se puede "
					" sobreescribir".format(filename))


	def _write_titulo(self, writer):

		titulo = ["fecha", "producto", "valor"]
		writer.writerow(titulo)


	def _write_items_de_tabla(self, writer, omip_db):

		for item in sorted(omip_db.items()):
			linea = self._formatea_to_save_csv(item)
			writer.writerow(linea)


	def _formatea_to_save_csv(self, item):

		#if not OmipDB.check_formato_item(item):
		#	raise ValueError("El item \"{}\" no tiene un formato válido")
		
		(fecha, producto, valor) = item
		formateado = [self._formaters["fecha"].formatea(fecha)] + \
					 [str(producto)] + 								  \
					 [self._formaters["float"].formatea(valor)]

		return formateado

