from ftplib import FTP,error_perm
import json,os,sys,logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s  - %(funcName)s - %(message)s')

class MConnection():
    ftp = None
    data = None

    def __init__(self,data):
        """
        :param data: dictionary with keys: name,ip,port,login,password
        """
        if type(data) != type(dict()):
            logging.debug('data is not dict in __init__')
            raise TypeError
        self.data = data
        self.func_dic = {'RETR': self.retr, 'STOR': self.stor, 'CWD': self.cwd}

    def retr(self,args):
        source_path = args[0]
        current_path = os.path.abspath('./')
        if args[1] != '':
           current_path = args[1]

        if os.path.isfile(current_path):
            with open(current_path, 'wb') as f:
                logging.debug(self.ftp.retrbinary('RETR ' + source_path, f.write))
        pass

    def stor(self,source_path,current_path):
        if os.path.isfile(current_path):
            with open(current_path, 'rb') as f:
                logging.debug(self.ftp.storbinary('STOR ' + r'Blocks\S.txt', f))
        pass

    def cwd(self,path):
        self.ftp.cwd(path)
        pass

    def connect(self):
        if self.ftp == None:
            logging.debug('ftp is None')
            ftp = FTP()
            try:
                res = ftp.connect(self.data['ip'],self.data['port'])
                if res.startswith('220'):
                    logging.debug(res)
            except Exception as e:
                logging.debug(str(e))
                return False

            #try to login
            if self.data['login'] == 'anonymous':
                try:
                    res = ftp.login()
                    if res.startswith('230'):
                        logging.debug(res)
                        return True
                except error_perm as e:
                    logging.debug(str(e))
                    return False

                try:
                    res = ftp.login(self.data['login'], self.data['password'])
                    if res.startswith('230'):
                        logging.debug(res)
                        return True

                except error_perm as e:
                    logging.debug(str(e))
                    return False

                logging.debug('Anonymous login failed')
                ftp = None
                return False
            else:
                try:
                    res = ftp.login(self.data['login'], self.data['password'])
                    logging.debug(res)
                    if res.startswith('230'):
                        return True
                except error_perm as e:
                    logging.debug(str(e))
                    return False

    def cmd_mode(self):
        s = '>>>'
        while True:
            res = input(s)
            splited = res.split(' ')
            self.data[splited[0]](splited[1:])
            if res == 'exit()':
                return 0

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
            f = open('connection.json', 'w')
            conns = []
            conns.append(self.data)
            json.dump(conns,f)
            f.close()