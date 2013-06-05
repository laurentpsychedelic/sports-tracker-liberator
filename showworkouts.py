#!/usr/bin/env python
# -*- coding: utf-8 -*-

from endomondo import Endomondo
from getpass import getpass
from datetime import timedelta
from sys import stdin, stderr
import time
from ConfigParser import ConfigParser

def get_email():
    stderr.write('Account name: ')
    return stdin.read()

def write_config_file(filename, email, password):
    config = ConfigParser()
    config.add_section('ACCOUNT INFO')
    config.set('ACCOUNT INFO', 'email', email)
    config.set('ACCOUNT INFO', 'password', password)
    with open(filename, 'w') as configfile:
        config.write(configfile)

def read_config_file(filename):
    with open(filename) as configfile:
        config = ConfigParser()
        config.read(filename)
        email = config.get('ACCOUNT INFO', 'email')
        password = config.get('ACCOUNT INFO', 'password')
        return { 'email': email, 'password': password }

if __name__ == "__main__":
    try:
        config_info = read_config_file('.endomondo')
        email = config_info['email']
        password = config_info['password']
    except:
        stderr.write('Profile not found, switch to manual input...\n')
        email = raw_input('Account name: ')
        password = getpass('Password: ')

    try:
        sports_tracker = Endomondo(email, password)
        write_config_file('.endomondo', email, password)
        for workout in sports_tracker.workout_list():
            print workout.summary + "<" + (workout.end_time - timedelta(seconds=time.timezone)).strftime("%Y-%m-%d %H:%M:%S") + ">\n"
            print str(workout.rawdata) + "\n\n"
    except:
        stderr.write('Error!')
        raise
