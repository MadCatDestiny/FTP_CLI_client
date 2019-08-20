from ftplib import FTP
from ftplib import error_perm
import json
import os
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s  - %(funcName)s - %(message)s')

class MConnection():
    ftp = None
    data = None

    def __init__(self, data):
        """
        :param data: dictionary with keys: name,ip,port,login,password
        """
        if type(data) != type(dict()):
            logging.debug('data is not dict in __init__')
            raise TypeError
        self.data = data
        self.func_dic = \
            {
                'RETR': self.retr,
                'STOR': self.stor,
                'CWD': self.cwd,
                'DELE': self.dele,
                'RMD': self.rmd,
                'MKD': self.mkd,
                'LIST': self.list,
                'SIZE': self.size,
                'SYST': self.syst,
                'CDUP': self.cdup,
                'PWD': self.pwd,
                'RNFR': self.rnfr
            }

    def rnfr(self, args):
        try:
            logging.debug(self.ftp.rename(args[0], args[-1]))
            return True
        except Exception as e:
            print(e)
            return False

    def pwd(self):
        return self.ftp.pwd()

    def cdup(self):
        try:
            logging.debug(self.ftp.sendcmd('CDUP'))
            return True
        except Exception as e:
            print(e)
            return False

    def syst(self):
        return self.ftp.sendcmd('SYST')

    def size(self, path):
        try:
            size = self.ftp.size(path)
            return size
        except Exception as e:
            print(e)
            return -1

    def list(self, path):
        try:
            res = ''
            if path == './':
                res = self.ftp.dir()
            else:
                res = self.ftp.dir(path)
            return res
        except Exception as e:
            return e

    def mkd(self, path):
        try:
            logging.debug(self.ftp.mkd(path))
            return True
        except Exception as e:
            print(e)
            return False

    def rmd(self, path):
        try:
            self.ftp.rmd(path)
            return True
        except Exception as e:
            print(e)
            return False

    def dele(self, path):
        try:
            logging.debug(self.ftp.delete(path))
            return True
        except Exception as e:
            print(e)
            return False

    def retr(self, args):
        """

        :param args: [<remote path>,<local path>]
        :return: True if transfer will be complete,else False
        """
        remote_path = args[0]
        local_path = os.path.abspath('./')
        if args[1] != '':
           local_path = args[1]

        with open(local_path, 'wb') as f:
            try:
                logging.debug(self.ftp.retrbinary('RETR ' + remote_path, f.write))
                return True
            except Exception as e:
                print(e)
                return False

    def stor(self, args):
        """

        :param args: [<remote path>,<local path>]
        :return:True if transfer will be complete,else False
        """
        remote_path = args[0]
        local_path  = args[1]
        if os.path.isfile(local_path):
            with open(local_path, 'rb') as f:
                try:
                    logging.debug(self.ftp.storbinary('STOR ' + remote_path, f))
                    return True
                except Exception as e:
                    print(e)
                    return False

    def cwd(self, path):
        """

        :param path: remote path
        :return: Tr
        """
        try:
            logging.debug(self.ftp.cwd(path))
            return True
        except Exception as e:
            print(e)
            return False

    def connect(self):
        if self.ftp is None:
            logging.debug('ftp is None')
            self.ftp = FTP()
            try:
                res = self.ftp.connect(self.data['ip'], self.data['port'])
                if res.startswith('220'):
                    logging.debug(res)
            except Exception as e:
                logging.debug(str(e))
                return False

            # try to login
            if self.data['login'] == 'anonymous':
                try:
                    res = self.ftp.login()
                    if res.startswith('230'):
                        logging.debug(res)
                        return True
                except error_perm as e:
                    logging.debug(str(e))
                    return False

                try:
                    res = self.ftp.login(self.data['login'], self.data['password'])
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
                    res = self.ftp.login(self.data['login'], self.data['password'])
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
            f = open('connection.json', 'rb')
            conns = json.load(f)
            f.close()
            logging.debug(str(conns))
            if self.data not in conns:
                conns.append(self.data)
            f = open('connection.json', 'wb')
            json.dump(conns, f)
            f.close()
        else:
            logging.debug('json not exists')
            f = open('connection.json', 'w')
            conns = []
            conns.append(self.data)
            json.dump(conns, f)
            f.close()