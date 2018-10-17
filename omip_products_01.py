

# Lista de productos
#OMIP_PRODUCTS = ("Jun-18", "Jul-18", "Aug-18", "Sep-18", "Oct-18", "Nov-18")
#OMIP_PRODUCTS = ("Q3-18", "Q4-18", "Q1-19", "Q2-19", "Q3-19", "Q4-19")
OMIP_PRODUCTS = ("Y-19", "Y-20", "Y-21", "Y-22")


# Direcciones de descarga
OMIP_URLS = {
			"Q1-18": "https://www.omip.pt/en/javali/get_full_chart/FTBQ1-18/0/1",
			"Q2-18": "https://www.omip.pt/en/javali/get_full_chart/FTBQ2-18/0/1",
			"Q3-18": "https://www.omip.pt/en/javali/get_full_chart/FTBQ3-18/0/1",
			"Q4-18": "https://www.omip.pt/en/javali/get_full_chart/FTBQ4-18/0/1",
			"Q1-19": "https://www.omip.pt/en/javali/get_full_chart/FTBQ1-19/0/1",
			"Q2-19": "https://www.omip.pt/en/javali/get_full_chart/FTBQ2-19/0/1",
			"Q3-19": "https://www.omip.pt/en/javali/get_full_chart/FTBQ3-19/0/1",
			"Q4-19": "https://www.omip.pt/en/javali/get_full_chart/FTBQ4-19/0/1", 
			 "Y-19": "https://www.omip.pt/en/javali/get_full_chart/FTBYR-19/0/1",
			 "Y-20": "https://www.omip.pt/en/javali/get_full_chart/FTBYR-20/0/1",
			 "Y-21": "https://www.omip.pt/en/javali/get_full_chart/FTBYR-21/0/1",
			 "Y-22": "https://www.omip.pt/en/javali/get_full_chart/FTBYR-22/0/1",
			 "Apr-18": "https://www.omip.pt/en/javali/get_full_chart/FTBMAPR-18/0/1",
			 "May-18": "https://www.omip.pt/en/javali/get_full_chart/FTBMMAY-18/0/1",
			 "Jun-18": "https://www.omip.pt/en/javali/get_full_chart/FTBMJUN-18/0/1",
			 "Jul-18": "https://www.omip.pt/en/javali/get_full_chart/FTBMJUL-18/0/1",
			 "Aug-18": "https://www.omip.pt/en/javali/get_full_chart/FTBMAUG-18/0/1",
			 "Sep-18": "https://www.omip.pt/en/javali/get_full_chart/FTBMSEP-18/0/1",
			 "Oct-18": "https://www.omip.pt/en/javali/get_full_chart/FTBMOCT-18/0/1",
			 "Nov-18": "https://www.omip.pt/en/javali/get_full_chart/FTBMNOV-18/0/1"}



class OmipProductos():

	def get_URL_for_producto(producto):

		OmipProductos.check_existe_producto(producto)

		url = OMIP_URLS[producto]
		return url


	def check_existe_producto(producto):

		#print("chequeando si existe el producto")
		if producto not in OMIP_PRODUCTS:
			#print("el producto no existe")
			raise ValueError("El producto \"{}\" no existe o no está definido".format(producto))


	def get_productos():

		return OMIP_PRODUCTS
	

