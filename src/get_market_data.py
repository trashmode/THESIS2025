import sqlite3


import time
from nempy import markets
from nempy.historical_inputs import loaders, mms_db, \
    xml_cache
from nempy.help_functions.helper_functions import update_rhs_values
from os import environ
start = time.time()
try:
    con = sqlite3.connect(environ.get("historical_mms"))
except:
    raise ValueError("No path in .env")
mms_db_manager = mms_db.DBManager(connection=con)
try:
    xml_cache_manager = xml_cache.XMLCacheManager(
        environ.get("xml_cache"))
except:
    raise ValueError("No path in .env")

# The second time this example is run on a machine this flag can
# be set to false to save downloading the data again.
download_inputs = False

if download_inputs:
    # This requires approximately 4 GB of storage.
    mms_db_manager.populate(start_year=2024, start_month=7,
                            end_year=2024, end_month=8)

    # This requires approximately 50 GB of storage.
    xml_cache_manager.populate_by_day(start_year=2024, start_month=6, start_day=1,
                                      end_year=2024, end_month=8, end_day=31)

raw_inputs_loader = loaders.RawInputsLoader(
    nemde_xml_cache_manager=xml_cache_manager,
    market_management_system_database=mms_db_manager)

print("--- %s seconds ---" % (time.time() - start))
