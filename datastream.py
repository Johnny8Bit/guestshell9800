
import requests
import urllib3
import time
import json
import sys
import re
import cli

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

send_top = 20
refresh_rate = 5

monitor_ip = "192.168.1.6"
monitor_port = "80"
monitor_api = f"http://{monitor_ip}:{monitor_port}/monitor"

include = "AP Name|Slot ID|Radio Type|Channel Utilization|Attached Clients|Channel Change Count|Last Channel Change Time"


def parse_output(cli_output):

    monitor_data = []
    for ap_data in cli_output:

        ap_metrics = []
        try:
            ap_name = re.match("\s+: (\S+)", ap_data).group(1)
        except AttributeError:
            continue
        ap_slot = re.search("Slot ID\s+: (\S+)", ap_data).group(1)
        ap_radio = re.search("Radio Type\s+: (.+)", ap_data).group(1)
        ap_chutil = re.search("Channel Utilization\s+: (\S+)", ap_data).group(1)
        ap_chutil = int(ap_chutil[:-1])
        ap_clients = re.search("Attached Clients\s+: (\S+)", ap_data).group(1)
        try:
            ap_changes = re.search("Channel Change Count\s+: (.+)", ap_data).group(1)
        except AttributeError:
            ap_changes = "-"
        try:
            ap_lastchange = re.search("Last Channel Change Time\s+: (.+)", ap_data).group(1)
        except AttributeError:
            ap_lastchange = "-"

        ap_metrics=(ap_name, ap_slot, ap_radio, ap_chutil, ap_clients, ap_changes, ap_lastchange)
        monitor_data.append(ap_metrics)

    return monitor_data


while True:

    try:
        output = parse_output(cli.cli(f"show ap auto-rf dot11 5ghz | include {include}").split("AP Name"))
        output_sorted = sorted(output, key=lambda x: x[3], reverse=True)[0:send_top] #sort by ch.util
        try:
            post = requests.post(monitor_api, data=json.dumps(output_sorted), verify=False, timeout=2)
            print(monitor_ip, post.status_code)
        except requests.exceptions.ConnectTimeout:
            print(monitor_ip, "Timeout")
        except requests.exceptions.ConnectionError:
            print(monitor_ip, "Connection error")
        time.sleep(refresh_rate)
    except KeyboardInterrupt:
        sys.exit()

