'''
scripts to run if connected online
'''
import os
from datetime import date,datetime

def online():

    cmd = '''
    PINGS=2
    TESTIP=8.8.8.8
    if ( ping -c $PINGS $TESTIP > /dev/null ) then
        echo "1"
    else
        echo "0"
    fi
    '''

    return int(os.popen(cmd).read())


def readpassphrase(__RDIR__):

    with open (os.path.join(__RDIR__,'.serverpi')) as f:
        lines = f.readlines()
        for line in lines:
            if 'serverpi_access_key = ' in line:
                private_key_pass = line[22:-1]

    return private_key_pass



def sync(SERIAL,conn):

    import pysftp
    from time import sleep
    from random import randint

    sleep(randint(10,600))  # Wait a random amount of time between 10 secs and 10 mins to limit overloading serverpi

    DATE = date.today().strftime("%d%m%Y")
    TIME = datetime.utcnow().strftime("%H%M%S")
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    data = [(SERIAL,TIME,DATE,)]

    conn.executemany("INSERT INTO PUSH (SERIAL,TIME,DATE) VALUES(?, ?, ?);", data )

    conn.commit()

    # if we are root, write to root dir
    user = os.popen('echo $USER').read().strip()

    if user == 'root': __RDIR__ = '/root'
    else: __RDIR__ = '/home/'+user

    key_pass = readpassphrase(__RDIR__)

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    file_path = os.path.join(__RDIR__,'sensor.db')

    private_key = os.path.join(__RDIR__,".ssh/id_rsa")  # can use password keyword in Connection instead

    for i in range (10):
        try:
            with pysftp.Connection(host="10.3.141.1", username="serverpi", private_key=private_key, private_key_pass=key_pass, cnopts=cnopts) as srv:
                srv.put(localpath=file_path,remotepath='/home/serverpi/datastaging/sensor_'+SERIAL+timestamp+'.db')  # To download a file, replace put with get
        except:
            if i < 9:
                print ('Upload failed - attempt {} of 10\nRetrying'.format(i+1))
                continue
            else:
                print ('Could not upload db to serverpi')
                return False

    return True
