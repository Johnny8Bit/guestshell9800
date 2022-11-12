from flask import Flask
from flask import request
from tabulate import tabulate
import json
import os

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

data_stream = Flask(__name__)


def generate_output(monitor_data):

    os.system("cls")
    headings = ["AP Name", "Slot", "Radio", "Ch.Util %", "Clients", "Ch.Changes", "Last Ch.Change"]
    print(tabulate(monitor_data, headers=headings))
    #print(f" {'AP Name':10} {'Slot':>10} {'Ch. Util':>10} {'Clients':>10}")
    #for bssid in sorted(ap, key=lambda x: ap[x]['RSSI'], reverse=True):
    #print(monitor_data)
    #for ap in sorted(monitor_data, key=lambda x: list(monitor_data.values())[0]["1"]["clients"]):
    #    print(type(ap))
    #print('END')




@data_stream.route('/monitor', methods = ['POST'])
def visualize():

    generate_output(json.loads(request.data))
    return 'OK', 200


if __name__ == '__main__':

    data_stream.run(host='0.0.0.0', port=9800, ssl_context='adhoc', debug=False)