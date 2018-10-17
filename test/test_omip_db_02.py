# -*- coding: cp1252 -*
import datetime as dt
import unittest

import configurador_test
from omip_db_02 import OmipDB

#DIR_EJEMPLOS = "..\\tests_omip_files"
DIR_EJEMPLOS = "tests_omip_files"

class OmipDB_Test(unittest.TestCase):
	
	def setUp(self):
		
		pass


	def tearDown(self):
		pass


	def test_save_item_to_db(self):

		db = OmipDB()
		fecha 	 = dt.datetime(2017, 10, 22)
		producto = "Q1-18"
		valor = 22.4
		#db.save_item(fecha, producto, valor)
		db[fecha, producto] = valor
		#self.assertEqual(db.get_item(fecha, producto), valor)
		self.assertEqual(db[fecha, producto], valor)


		db = OmipDB()
		fecha 	 = dt.datetime(2017, 10, 22)
		producto = "Q1-18"
		valor = 22.4
		db.save_item(fecha, producto, valor)
		#db[fecha, producto] = valor

		self.assertEqual(db.get_item(fecha, producto), valor)
		#self.assertEqual(db[fecha, producto], valor)


	def test_update(self):

		db1 = OmipDB()
		fecha 	 = dt.datetime(2017, 10, 22)
		producto = "Q1-18"
		valor 	 = 22.4
		db1.save_item(fecha, producto, valor)
		#db[fecha, producto] = valor

		db2 = OmipDB()
		fecha = dt.datetime(2017, 10, 23)
		db1.save_item(fecha, producto, valor)
		db1.update(db2)
		self.assertEqual(len(db1.items()), 2)


	def test_get_items_sin_indicar_fecha_muestra_todos_los_values(self):

		db = OmipDB()
		db.save_item(dt.datetime(2017, 10, 1), "Q1-18", 10.44)
		db.save_item(dt.datetime(2017, 10, 1), "Q2-18", 20.44)
		db.save_item(dt.datetime(2017, 10, 2), "Q1-18", 10.55)
		db.save_item(dt.datetime(2017, 10, 2), "Q2-18", 20.55)
		db.save_item(dt.datetime(2017, 10, 3), "Q1-18", 11.43)

		values = db.get_items()

		self.assertEqual(len(values), 5)
		#print("values: ", values)
		self.assertEqual(values[dt.datetime(2017, 10, 1), "Q1-18"], 10.44)
		self.assertEqual(values[dt.datetime(2017, 10, 1), "Q2-18"], 20.44)
		self.assertEqual(values[dt.datetime(2017, 10, 2), "Q1-18"], 10.55)
		self.assertEqual(values[dt.datetime(2017, 10, 2), "Q2-18"], 20.55)
		self.assertEqual(values[dt.datetime(2017, 10, 3), "Q1-18"], 11.43)


	def test_raise_error_si_get_items_con_fechas_fin_menor_que_fecha_ini(self):

		ini = dt.datetime(2017, 9, 28) # 28/09/2017
		fin = dt.datetime(2017, 9, 1) # 01/09/2017

		with self.assertRaises(ValueError):
			db = OmipDB()
			db.get_items(date_ini = ini , date_fin = fin)


	def test_get_items_entre_dos_fechas(self):

		db = OmipDB()
		db.save_item(dt.datetime(2017, 10, 1), "Q1-18", 10.44)
		db.save_item(dt.datetime(2017, 10, 1), "Q2-18", 20.44)
		db.save_item(dt.datetime(2017, 10, 2), "Q1-18", 10.55)
		db.save_item(dt.datetime(2017, 10, 2), "Q2-18", 20.55)
		db.save_item(dt.datetime(2017, 10, 3), "Q1-18", 11.43)

		ini = dt.datetime(2017, 10, 1) # 01/10/2017
		fin = dt.datetime(2017, 10, 2) # 02/10/2017
		values = db.get_items(date_ini = ini , date_fin = fin)

		self.assertEqual(len(values), 4)
		self.assertEqual(values[dt.datetime(2017, 10, 1), "Q1-18"], 10.44)
		self.assertEqual(values[dt.datetime(2017, 10, 1), "Q2-18"], 20.44)
		self.assertEqual(values[dt.datetime(2017, 10, 2), "Q1-18"], 10.55)
		self.assertEqual(values[dt.datetime(2017, 10, 2), "Q2-18"], 20.55)


	def test_fecha_in_date_range(self):

		ini = dt.datetime(2017, 10, 1) # 01/10/2017
		fin = dt.datetime(2017, 10, 2) # 02/10/2017
		
		db = OmipDB()
		db.save_item(dt.datetime(2017, 10, 1), "Q1-18", 10.44)
		db.save_item(dt.datetime(2017, 10, 1), "Q2-18", 20.44)
		db.save_item(dt.datetime(2017, 10, 2), "Q1-18", 10.55)
		db.save_item(dt.datetime(2017, 10, 2), "Q2-18", 20.55)
		db.save_item(dt.datetime(2017, 10, 3), "Q1-18", 11.43)

		#print("item: ", db[dt.datetime(2017, 10, 1), "Q1-18"])
		#print("está el item? ", (dt.datetime(2017, 10, 1), "Q1-18") in db)

		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 9, 30), ini, fin), False)
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 10, 1), ini, fin), True)
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 10, 2), ini, fin), True)
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 10, 3), ini, fin), False)

		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 9, 30), None, fin), True)
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 10, 1), None, fin), True)
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 10, 2), None, fin), True)
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 10, 3), None, fin), False)

		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 9, 30), ini, None), False)
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 10, 1), ini, None), True)
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 10, 2), ini, None), True)
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 10, 3), ini, None), True)

		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 9, 30), None, None), True)
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 10, 1), None, None), True)
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 10, 2), None, None), True)
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 10, 3), None, None), True)

		ini = dt.datetime(2017, 11, 21) # 01/10/2017
		fin = dt.datetime(2017, 11, 23) # 02/10/2017
		self.assertEqual(db._fecha_in_date_range(dt.datetime(2017, 11, 22), ini, fin), True)


	def test_items(self):

		db = OmipDB()

		item1 = (dt.datetime(2017, 10, 22), "Q1-18", 1)
		item2 = (dt.datetime(2017, 10, 22), "Q2-18", 2)
		item3 = (dt.datetime(2017, 10, 22), "Q3-18", 3)
	
		#db.save_item(item1[0], item1[1], item1[2]) # OmipDB.save_item(fecha, producto, valor)
		#db.save_item(item2[0], item2[1], item2[2])
		#db.save_item(item3[0], item3[1], item3[2])

		db[item1[0], item1[1]] = item1[2] # OmipDB[fecha, producto] = valor
		db[item2[0], item2[1]] = item2[2]
		db[item3[0], item3[1]] = item3[2]

		self.assertEqual(len(db.items()), 3)
		self.assertEqual(db.items(), (item1, item2, item3))


	def test_contains(self):

		db = OmipDB()

		t1 = dt.datetime(2017, 10, 22)
		p1 = "Q1-18"
		db[t1, p1] = 1

		self.assertEqual(db.contiene(dt.datetime(2017, 10, 22), "Q1-18"), True)
		self.assertEqual(db.contiene(dt.datetime.now(), "PRODUCTO NO EXISTENTE"), False)
		self.assertEqual((dt.datetime(2017, 10, 22), "Q1-18") in db, True)
		self.assertEqual((dt.datetime.now(), "PRODUCTO NO EXISTENTE") in db, False)


	def test_number_of_items_in_db(self):

		db = OmipDB()
		#db.save_item(dt.datetime(2017, 10, 22), "Q1-18", 1) # OmipDB.save_item(fecha, producto, valor)
		#db.save_item(dt.datetime(2017, 10, 22), "Q2-18", 2)
		#db.save_item(dt.datetime(2017, 10, 22), "Q3-18", 3)
		db[dt.datetime(2017, 10, 22), "Q1-18"] = 1 # OmipDB[fecha, producto] = valor
		db[dt.datetime(2017, 10, 22), "Q2-18"] = 2
		db[dt.datetime(2017, 10, 22), "Q3-18"] = 3

		self.assertEqual(len(db), 3) 
		self.assertEqual(db.num_items(), 3)


	def test_check_formato_item(self):

		item_ok = (dt.datetime(2017,10,7), "Q1-18", 20.2)
		item_mal_1 = ()
		item_mal_2 = ("mal", "mal", "mal")
		item_mal_3 = (("mal", "mal"), "mal")
		item_mal_4 = (dt.datetime(2017, 10, 20), 22.2, "mal")
		item_mal_5 = ((dt.datetime(2017, 10, 20), "Q1-18"), 22.2)
		item_mal_6 = (dt.datetime(2017, 10, 20), "Q1-18", "mal")

		self.assertEqual(OmipDB.check_formato_item(item_ok), True)
		self.assertEqual(OmipDB.check_formato_item(item_mal_1), False)
		self.assertEqual(OmipDB.check_formato_item(item_mal_2), False)
		self.assertEqual(OmipDB.check_formato_item(item_mal_3), False)
		self.assertEqual(OmipDB.check_formato_item(item_mal_4), False)
		self.assertEqual(OmipDB.check_formato_item(item_mal_5), False)
		self.assertEqual(OmipDB.check_formato_item(item_mal_6), False)


if __name__ == '__main__':
	unittest.main() # runs any method that starts with the prefix "test", no
					# matter how many classes we create within a given Python module

	'''
	test = OmipDB_Test()
	test.setUp()
	test.test_fecha_in_date_range()
	'''

	