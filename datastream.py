from datetime import datetime

import json
import os

from flask import Flask
from flask import request
from tabulate import tabulate

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

data_stream = Flask(__name__)


def generate_output(monitor_data):

    os.system("cls")
    print("Last update:", str(datetime.now())[:-7], "\n")
    headings = ["AP Name", "Slot", "Radio", "Ch.Util %", "Clients", "Ch.Changes", "Last Ch.Change"]
    print(tabulate(monitor_data, headers=headings))


@data_stream.route('/monitor', methods = ['POST'])
def visualize():

    generate_output(json.loads(request.data))
    return 'OK', 200


if __name__ == '__main__':

    data_stream.run(host='0.0.0.0', port=9800, ssl_context='adhoc', debug=False)