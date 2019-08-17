from ftplib import FTP
from connection import MConnection
import json,os,sys,logging,datetime
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
"""
Example:
data = [
            {
            'name':'Name of connection'
            'ftp':'192.168.0.105',
            'port':21,
            'login':'hb1998',
            'password':'l0gpass'
            },
            {
            'name':'Name of connection2'
            'ftp':'192.168.0.105',
            'port':21,
            'login':'hb19982',
            'password':'l0gpass2'
            }
        ]
"""
def new_connection():
    data = {}
    ip = input('Enter ip: ')
    port = int(input('Enter port: '))
    data.setdefault('ip',ip)
    data.setdefault('port', port)
    flag = None

    while flag == None:
        flag = input('Do you want to log in as a specific or anonymous user? <s/a>')
        if flag == 's':
            login = input('Enter login: ')
            password = input('Enter passord:')
            data.setdefault('login',login)
            data.setdefault('password',password)
        elif flag == 'a':
            data.setdefault('login','anonymous')
            data.setdefault('password','guest')
        else:
            flag = None
    data.setdefault('name','_'.join([ip,datetime.date.today()]))
    conn = MConnection(data)
    logging.debug('_'.join([ip,datetime.date.today().strftime("%d.%m.%Y") ]))
    save = input('Do you want save connection? <y/n>')
    if save == 'y':
        logging.debug('save')
        name = input('Enter name: ')
        #TODO: add check for name
        data.setdefault('name',name)
        conn = MConnection(data)
        conn.save()

    return conn

def menu():
    reply = 0
    connections_list = []
    #TODO:add opportunity delete connection from list
    while reply not in range(1,2 + len(connections_list)):
        print('1 - New connection')
        connections_list = [] #list with saved connections
        if os.path.exists('./connections.json'):
            f = open('connections.json','rb')
            connections_list = json.load(f)
            f.close()
            for item,i in connections_list,range(len(connections_list)):
                print(str(i+2) + ' - {0} ( {1}::{2}'.format(item['name'],item['ip'],item['port']))
        reply = int(input('>>>'))
        flag = reply in range(1,2+len(connections_list))
        logging.debug('reply in range: %s' %str(flag))
        if reply == 1 and flag:
            return new_connection()
        elif flag:
            return MConnection(connections_list[reply-2])

########################################################################################################################
#----------------------------------------------------------------------------------------------------------------------#
########################################################################################################################
def main():
    conn = None
    while conn == None:
        conn = menu()
        if conn.connect():
            conn.cmd_mode()
        else:
            conn = None

