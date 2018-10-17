from unittest import TestLoader, TextTestRunner, TestSuite

import configurador_test

from test_omip_data_02 import OmipData_Test
from test_omip_file_download_02 import OmipDownload_Test
from test_omip_file_reader_05 import OmipRawDataReader_Test, OmipStoredDataReader_Test
from test_omip_file_writer_02 import OmipStoredDataWriter_Test
from test_omip_productos_01 import OmipProductos_Test
from test_omip_db_01 import OmipDB_Test

'''
if __name__ == "__main__":

	loader = TestLoader()

	# SUITE OMIP DOWNLOAD:
	suite_omip = TestSuite((
		loader.loadTestsFromTestCase(OmipData_Test),
		loader.loadTestsFromTestCase(OmipDownload_Test),
		loader.loadTestsFromModule(OmipRawDataReader_Test),
		loader.loadTestsFromModule(OmipStoredDataReader_Test),
		loader.loadTestsFromModule(OmipStoredDataWriter_Test),
		loader.loadTestsFromModule(OmipDB_Test),
		loader.loadTestsFromModule(OmipProductos_Test)
		#loader.loadTestsFromTestCase(ParserStr_Test),
		#loader.loadTestsFromTestCase(EncodingUtil_Test),
		))


	runner = TextTestRunner(verbosity = 2)
	#runner.run(suite_medicion)
	runner.run(suite_omip)
'''

import nose
nose.main()

