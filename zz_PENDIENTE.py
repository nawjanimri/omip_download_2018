Tareas pendientes
-----------------

# 0. Escribir test para _check_formato_item en archivo test_omip_file_writer_01.py
1. Montar base de datos de datos omip: omip_db_01.py ??? --> LISTO!

		La idea es encapsular ahí la estructura de almacenamiento de datos de omip.
		Actualmente está en un data {} en formato: data[(fecha, producto)] = valor

			Propuestas:

				def _save_item_to_bd(self, fecha, producto, valor):

				def _get_item_from_bd(self, fecha, producto):


2. Crear test para omip_file_writer_01.py --> LISTO!