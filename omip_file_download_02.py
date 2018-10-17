import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

#import configurador_test
from omip_products_01 import OmipProductos


# URL: http://kazuar.github.io/scraping-tutorial/
# URL: https://stackoverflow.com/questions/15646813/file-download-via-post-form
# URL: https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
# URL: https://stackoverflow.com/questions/35747033/how-to-download-files-in-python-with-post-request

'''
OMIP_URLS = {"Q1-18": "https://www.omip.pt/en/javali/get_chart/FTBQ1-18/0/0/0/1",
			 "Q2-18": "https://www.omip.pt/en/javali/get_chart/FTBQ2-18/0/0/0/1", 
			 "Q3-18": "https://www.omip.pt/en/javali/get_chart/FTBQ3-18/0/0/0/1",
			 "Q4-18": "https://www.omip.pt/en/javali/get_chart/FTBQ4-18/0/0/0/1",
			 "Q1-19": "https://www.omip.pt/en/javali/get_chart/FTBQ1-19/0/0/0/1",
			 "Q2-19": "https://www.omip.pt/en/javali/get_chart/FTBQ2-19/0/0/0/1",
			 "Q3-19": "https://www.omip.pt/en/javali/get_chart/FTBQ3-19/0/0/0/1",
			 "Q4-19": "https://www.omip.pt/en/javali/get_chart/FTBQ4-19/0/0/0/1"
			 }
'''

class OmipFileDownload():

	#def __init__(self, filepath):

		#self._filepath = filepath

	def __init__(self):

		pass


	def download_product_raw_file(self, producto, filepath): 
		
		self._producto = producto
		OmipProductos.check_existe_producto(producto)

		raw = self._download_raw_content(self._producto)
		self._save_raw_data_to_file(raw, filepath)


	def _download_raw_content(self, producto):

		# Eiminar los warnings del requests:
		# https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho
		# https://stackoverflow.com/questions/15445981/how-do-i-disable-the-security-certificate-check-in-python-requests/15445989
		# to avoid hiding all warnings but "InsecureRquestWarning", set "category = InsecureRequestWarning" 
		requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

		#download_url = OMIP_URLS[producto]
		download_url = OmipProductos.get_URL_for_producto(producto)
		result = requests.get(download_url, verify = False)

		return result.text


	def _save_raw_data_to_file(self, raw_content, filepath):

		self._check_file_no_existe_todavia(filepath)

		with open(filepath, 'w', errors="ignore") as file:
			for line in raw_content:
				#print("linea: ", line)
				file.write(line)


	def _check_file_no_existe_todavia(self, filepath):

		if os.path.isfile(filepath):
			filename = os.path.basename(filepath)
			raise FileExistsError("El archivo \"{}\" ya existe y no se puede "
					" sobreescribir".format(filename))


