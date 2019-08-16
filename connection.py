from ftplib import FTP
import json,os,sys,logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')

class MConnection():
    def __init__(self,data):
        """
        :param data: dictionary with keys: name,ip,port,login,password
        """
        if type(data) != type(dict()):
            raise TypeError
        self.data = data

    def connect(self):
        pass

    def is_available(self):
        pass

    def cmd_mode(self):
        pass

    def save(self):
        if os.path.exists('./connections.json'):
            logging.debug('json exists')
            f = open('connection.json','rb')
            conns = json.load(f)
            f.close()
            logging.debug(str(conns))
            if self.data not in conns:
                conns.append(self.data)
            f = open('connection.json', 'wb')
            json.dump(conns,f)
            f.close()
        else:
            logging.debug('json not exists')
            f = open('connection.json', 'wb')
            conns = []
            conns.append(self.data)
            json.dump(conns,f)
            f.close()