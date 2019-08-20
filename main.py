from connection import MConnection
import json
import os
import logging
import datetime
import argparse
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s  - %(funcName)s - %(message)s')
"""
Example:
data = [
            {
            'name':'Name of connection'
            'ip':'192.168.0.105',
            'port':21,
            'login':'hb1998',
            'password':'l0gpass'
            },
            {
            'name':'Name of connection2'
            'ip':'192.168.0.105',
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
    data.setdefault('ip', ip)
    data.setdefault('port', port)
    flag = None

    while flag is None:
        flag = input('Do you want to log in as a specific or anonymous user? <s/a>')
        if flag == 's':
            login = input('Enter login: ')
            password = input('Enter passord:')
            data.setdefault('login', login)
            data.setdefault('password', password)
        elif flag == 'a':
            data.setdefault('login', 'anonymous')
            data.setdefault('password', 'guest')
        else:
            flag = None
    data.setdefault('name', ip + '_' + datetime.date.today().strftime("%d.%m.%Y"))
    conn = MConnection(data)
    logging.debug(ip + '_' + datetime.date.today().strftime("%d.%m.%Y"))
    save = input('Do you want save connection? <y/n>')
    if save == 'y':
        logging.debug('save')
        flag = False
        name = ''
        while not flag:
            name = input('Enter name: ')
            data['name'] = name
            if flag != '':
                for char in name:
                    if char != ' ':
                        flag = True

        data.setdefault('name', name)
        conn = MConnection(data)
        conn.save()

    return conn


def delete_cn(num):
    f = open('connection.json', 'r')
    data = json.load(f)
    data.pop(num-2)
    logging.debug('data len after remove' + str(len(data)))
    f.close()
    f = open('connection.json', 'w')
    json.dump(data, f)
    f.close()


def menu():
    reply = 0
    connections_list = []
    logging.debug('Start menu')
    while reply not in range(1, 2 + len(connections_list)):
        print('-1 - Close program')
        print('0 - Delete connection')
        print('1 - New connection')
        connections_list = []  # list with saved connections
        path = os.path.abspath('./')
        logging.debug(path + '\\connections.json')
        if os.path.isfile(path + '\\connection.json'):
            logging.debug('json exists')
            f = open('connection.json', 'r')
            connections_list = json.load(f)
            f.close()
            logging.debug('len(connections_list): ' + str(len(connections_list)))
            i = 0
            for item in connections_list:
                print(str(i+2) + ' - {0} ( {1}::{2} )'.format(item['name'], item['ip'], item['port']))
                i += 1
        reply = int(input('>>>'))
        if reply == -1:
            return -1
        flag = reply in range(1, 2+len(connections_list))
        logging.debug('reply in range: %s' % str(flag))
        if reply == 1:
            return new_connection()
        elif reply == 0:
            rp = int(input('Enter number of connection? Enter 0 to exit'))
            logging.debug(str(rp in range(1, 2 + len(connections_list))))
            if rp in range(1, 2 + len(connections_list)):
                logging.debug('reply in range for delete')
                delete_cn(rp)
        elif flag:
            return MConnection(connections_list[reply-2])


def interactive_main():
    conn = None
    while conn is None:
        logging.debug('Conn is none')
        conn = menu()
        if conn == -1:
            return
        if conn.connect():
            conn.cmd_mode()
        else:
            conn = None


def cmd_main(args):
    splited = args.login.split('@')
    data = \
        {
            'name': datetime.date.today().strftime("%d.%m.%Y") + '_withargs',
            'ip': splited[1],
            'port': args.port,
            'login': splited[0]
        }
    if args.passw:
        data.setdefault('password', args.passw)
    else:
        data.setdefault('password', '')
    mc = MConnection(data)
    if mc.connect():
        if args.retr and len(args.retr) == 2:
            print('RETR: %s' % mc.retr(args.retr))
        if args.stor and len(args.stor) == 2:
            print('STOR: %s' % mc.stor(args.stor))
        if args.dele:
            print('DELE: %s' % mc.dele(args.dele))
        if args.rmd:
            print('RMD: %s' % mc.rmd(args.rmd))
        if args.mkd:
            print('MKD: %s' % mc.mkd(args.mkd))
        if args.list:
            print('LIST:\n%s' % mc.list(args.list))
        if args.cwd:
            print('CWD {0}\n{1}'.format(mc.cwd(args.cwd), args.cwd))
        if args.size:
            print('SIZE: %s' % mc.size(args.size))
        if args.syst:
            print('SYST: %s' % mc.syst())
        if args.cdup:
            print('CDUP: %s' % mc.cdup())
        if args.rnfr and len(args.rnfr) == 2:
            print('RNFR {0} RNTO {1} : {2}'.format(args.rnfr[0], args.rnfr[1], mc.rnfr(args.rnfr)))
        if args.pwd:
            print('PWD: %s' % mc.pwd())

########################################################################################################################
#----------------------------------------------------------------------------------------------------------------------#
########################################################################################################################


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('login', help='user@ip')
    parser.add_argument('port', help='port in server', type=int, default=21)
    parser.add_argument('-p', '--passw', help='Password')
    parser.add_argument('-r', '--retr', help='RETR <server path> <local path>', nargs='+')
    parser.add_argument('-s', '--stor', help='STOR <server path> <local path>', nargs='+')
    parser.add_argument('-i', '--interactive', help='Interactive mode', action='count')
    parser.add_argument('-d', '--dele', help='DELE <server path>')
    parser.add_argument('--rmd', help='RMD <server path>')
    parser.add_argument('--mkd', help='MKD <server path>')
    parser.add_argument('-l', '--list', help='LIST <server path>*', action='store_const', const='./')
    parser.add_argument('-c', '--cwd', help='CWD <server path>')
    parser.add_argument('--size', help='SIZE <server path>')
    parser.add_argument('--syst', help='SYST', action='count')
    parser.add_argument('--cdup', help='CDUP', action='count')
    parser.add_argument('--rnfr', help='RNFR <rename from> <rename to>', nargs='+')
    parser.add_argument('--pwd', help='PWD', action='count')

    args = parser.parse_args()
    if args.interactive:
        interactive_main()
    else:
        cmd_main(args)


if __name__ == '__main__':
    main()
