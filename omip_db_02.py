import datetime as dt

class OmipDB():

	def __init__(self):

		# Estructura del data: 
		# Ej: data[(datetime(2017, 8, 1), "Q1-18")] = 44.5
		self._data = {}


	def save_item(self, fecha, producto, valor):

		self._data[(fecha, producto)] = valor # Ej: data[(datetime(2017, 8, 1), "Q1-18")] = 44.5


	def update(self, new_data):

		#print("tipo de new_data: ", type(new_data))
		#print("new_data: ", new_data)
		self._data.update(new_data._data) # actualiza el {} con otro {}
		

	def get_fechas(self):

		fechas = [item[0] for item in self._data.items()] # se toma sólo la fecha de cada item {(21/10/2017, Q1-18): 40.5, ...
		fechas = list(set(fechas))
		return fechas


	def get_item(self, fecha, producto):

		return self._data[(fecha, producto)]


	def get_items(self, product_list=None, date_ini=None, date_fin=None):

		self._check_fechas(date_ini, date_fin)

		db = OmipDB()

		if product_list:
			for (fecha, producto_name, valor) in self._get_items_iter():
				#print("fecha y product name", (fecha, producto_name))
				if self._fecha_in_date_range(fecha, date_ini, date_fin) and (producto_name in product_list):	
						db.save_item(fecha, producto_name, valor)
		else:
			for (fecha, producto_name, valor) in self._get_items_iter():
				#print("fecha y product name", (fecha, producto_name))
				if self._fecha_in_date_range(fecha, date_ini, date_fin):
					db.save_item(fecha, producto_name, valor)
					#valores[(fecha, producto_name)] = self._data[(fecha, producto_name)]
		return db


	def _check_fechas(self, date_ini, date_fin):

		def check_fecha_es_superior_a_hoy(fecha):
			hoy = dt.datetime.now()
			if fecha > hoy:
				raise ValueError("La fecha no puede ser superior al día de hoy :"
					" ({} > {})".format(fecha, hoy))

		if date_ini:
			check_fecha_es_superior_a_hoy(date_ini)

		if date_fin:
			check_fecha_es_superior_a_hoy(date_fin)

		if date_ini and date_fin:
			if date_ini > date_fin:
				raise ValueError("La fecha de inicio no puede ser superior a la fecha "
					"de fin: {} < {}".format(date_ini, date_fin))


	def _get_items_iter(self): # iterador

		for item in self._data:
			yield (item[0], item[1], self._data[(item[0], item[1])]) # (21/10/2017, Q1-18, 40.5)


	def _fecha_in_date_range(self, fecha, date_ini, date_fin):
		#Hay que chequear en tantos pasos porque es posible que date_ini o date_fin sean None

		cumple_ini = False
		cumple_fin = False

		if date_ini:
			if fecha>= date_ini:
				cumple_ini = True
		else:
			cumple_ini = True
		
		if date_fin:
			if fecha<= date_fin:
				cumple_fin = True
		else:
			cumple_fin = True

		if cumple_ini and cumple_fin:
			return True
		else:
			return False


	def items(self):
		''' Iterador que devuelve tuplas con (fecha, producto, valor)'''
		#return [(item[0], item[1], self._data[(item[0], item[1])]) for item in self._data]
		return tuple(item for item in self._get_items_iter())
	

	def __getitem__(self, item_key):
		# valor = midict[fecha, producto]

		# Acceso mediante índice a la base de datos
		# https://stackoverflow.com/questions/6486387/implement-list-like-index-access-in-python
		#print("item_key: ", item_key, "type: ", type(item_key))
		fecha, producto = item_key
		return self._data[(fecha, producto)]


	def __setitem__(self, item_key, valor):
		# midict[fecha, producto] = valor

		fecha, producto = item_key
		self._data[(fecha, producto)] = valor


	def contiene(self, fecha, producto):

		return (fecha, producto) in self._data


	def __contains__(self, key):
		# (fecha, producto) in midict

		(fecha, producto) = key
		return self.contiene(fecha, producto)


	def num_items(self):

		return len(self._data)


	def __len__(self):

		return len(self._data)


	@classmethod
	def check_formato_item(cls, item):

		try:
			(fecha, producto, valor) = item
		except:
			return False

		try:
			assert type(fecha) is dt.datetime
			assert type(producto) is str
			assert type(valor) is float
		except:
			return False

		return True