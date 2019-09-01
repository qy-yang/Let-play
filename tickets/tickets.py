# -*- code=utf-8 -*-

'''
Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h, --help  Check help
    -g          China High-speed Railway
    -d          China Railway High-speed
    -t          Express train
    -k          Ordinary train
    -z          Non-stop train

Example:
    tickets Beijing Shanghai 2016-10-10
    tickets -dg Chengdu Nanjing 2016-10-10
'''

from docopt import docopt
from stations import stations
import requests
from prettytable import PrettyTable
from colorama import init, Fore

init()


class TrainsCollections():
    header = 'TrainNo Station Time Duration FirstClass SecondClass SoftSleeper HardSleeper HardSeat NoSeat'.split()

    def __init__(self, available_trains, available_place, ptions):
        self.available_trains = available_trains
        self.available_place = available_place
        self.options = options

    @property
    def train(self):
        # property decorate, convert get method to object property
        for raw_train in self.available_trains:
            raw_train_list = raw_train.split('|')
            train_no = raw_train_list[3]
            initial = train_no[0].lower
            duration = raw_train_list[10]
            if not self.options or initial in self.options:
                # Color departure station and time as green, arrival station and time as red
                train = [train_no, 
                         '\n'.join([Fore.GREEN + self.available_place[raw_train_list[6]] + Fore.RESET,
                               Fore.RED + self.available_place[raw_train_list[7]] + Fore.RESET]),
                         '\n'.join([Fore.GREEN + self.available_place[raw_train_list[8]] + Fore.RESET,
                               Fore.RED + self.available_place[raw_train_list[9]] + Fore.RESET]),
                         duration,
                         raw_train_list[-6] if raw_train_list[-6] else '--',
                         raw_train_list[-7] if raw_train_list[-7] else '--',
                         raw_train_list[-15] if raw_train_list[-15] else '--',
                         raw_train_list[-8] if raw_train_list[-8] else '--',
                         raw_train_list[-14] if raw_train_list[-14] else '--',
                         raw_train_list[-11] if raw_train_list[-11] else '--',
                         raw_train_list[-9] if raw_train_list[-9] else '--',]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)
    


def cli():
    '''Command-line interface'''
    arguments = docopt(__doc__)
    # print(arguments)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # construct url
    url = ('https://kyfw.12306.cn/otn/lcxxcx/query?'
           'purpose_codes=ADULT&queryDate={}&'
           'from_station={}&to_station={}').format(
        date, from_station, to_station)

    # Not verify certificate
    r = requests.get(url, verify=False)
    available_trains = r.json()['data']['result']
    available_place = r.json()['data']['map']
    options = ''.join([key for key, item in arguments.item() if value is True])
    TrainsCollections(available_trains, available_place, options).pretty_print()


if __name__ == '__main__':
    cli()