from datetime import datetime

import json
import sys
import os

from flask import Flask
from flask import request
from tabulate import tabulate

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

text_monitor = Flask(__name__)


def generate_output(monitor_data):

    if platform == "win32": os.system("cls")
    elif platform == "linux": os.system("clear")
    print("Last update:", str(datetime.now())[:-7], "\n")
    headings = ["AP Name", "Slot", "Radio", "Ch.Util %", "Clients", "Ch.Changes", "Last Ch.Change"]
    print(tabulate(monitor_data, headers=headings))


@text_monitor.route('/monitor', methods = ['POST'])
def visualize():

    generate_output(json.loads(request.data))
    return 'OK', 200


if __name__ == '__main__':

    platform = sys.platform
    text_monitor.run(host='0.0.0.0', port=80, debug=False)