'''
If we do not already have a database (or wish to delete and replace the existing one) run

python -m serverpi.db new
            or
python -m serverpi.db + user input

'''

import os,sys,sqlite3
from .__init__ import __RDIR__,filename,conn
from .builddb import builddb

## no accidental overwrites
if 'new' not in sys.argv:
    assert 'yes' == input('Please type "yes" to delete the old database (if it exists) and create a new one')


#remove and create new
conn.close()

os.remove(__RDIR__+filename)

conn = sqlite3.connect(__RDIR__+filename)

builddb(conn)

conn.close()
print('A new database has now been created')

 #
 # [str(i) for i in (location['gpstime'],location['lat'],location['lon'],location['alt'],int(location['nsat']),location['PM1'],location['PM2.5'],location['PM10'])]
