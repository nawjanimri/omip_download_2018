import datetime as dt

#import configurador

class OmipStats():

	def __init__(self):

		self._stats = {}
		self.reset_stats()


	def reset_stats(self):
		
		self._stats["fecha_update"] = None
		self._stats["num_registros"] = 0
		self._stats["num_registros_added"] = 0
		self._stats["fecha_ini"] = None
		self._stats["fecha_fin"] = None
		self._stats["fecha_last_update_from_server"] = None
		self._stats["fecha_ini_data_last_update_from_server"] = None
		self._stats["fecha_fin_data_last_update_from_server"] = None
		self._stats["num_registros_last_update_from_server"] = 0


	def update(self, data, 
				fecha_last_update_from_server = None,
				fecha_ini_data_last_update_from_server = None, 
				fecha_fin_data_last_update_from_server = None, 
				num_registros_last_update_from_server = 0):

		self._stats["fecha_update"] = dt.datetime.now()

		data_list = sorted(list(data.items())) # hace el list con los items completos del dict
		
		num_registros_antes = self._stats["num_registros"]
		self._stats["num_registros"] = len(data_list)
		self._stats["num_registros_added"] = self._stats["num_registros"] - num_registros_antes 
		
		if data_list:
			omip_ini = data_list[0]		# (20/11/2017, Q2-18, 40.06)
			omip_fin = data_list[-1]	# (23/11/2017, Q2-18, 47.23)
			fecha_ini = omip_ini[0] 	# 20/11/2017
			fecha_fin = omip_fin[0] 	# 23/11/2017
		else:
			fecha_ini = None
			fecha_fin = None

		self._stats["fecha_ini"] = fecha_ini
		self._stats["fecha_fin"] = fecha_fin

		if fecha_last_update_from_server:
			self._stats["fecha_last_update_from_server"] = fecha_last_update_from_server
			self._stats["fecha_ini_data_last_update_from_server"] = fecha_ini_data_last_update_from_server
			self._stats["fecha_fin_data_last_update_from_server"] = fecha_fin_data_last_update_from_server
			self._stats["num_registros_last_update_from_server"] = num_registros_last_update_from_server


	def get_stats(self, param):

		try:
			return self._stats[param]

		except KeyError:

			return ""


	def get_items(self):

		return self._stats.copy().items()