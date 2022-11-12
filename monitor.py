
import requests
import urllib3
import time
import json
import re
import cli

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

send_top = 20

monitor_ip = "192.168.1.6"
monitor_port = "9800"
monitor_api = f"https://{monitor_ip}:{monitor_port}/monitor"

monitor_data = []

while True:

    include = "AP Name|Slot ID|Radio Type|Channel Utilization|Attached Clients|Channel Change Count|Last Channel Change Time"
    output = cli.cli(f"show ap auto-rf dot11 5ghz | include {include}").split("AP Name")

    for ap_data in output:

        ap_metrics = []
        try:
            ap_name = re.match("\s+: (\S+)", ap_data).group(1)
        #    ap_metrics.append(ap_name)
        except AttributeError:
            continue
        ap_slot = re.search("Slot ID\s+: (\S+)", ap_data).group(1)
        #ap_metrics.append(ap_slot)

        ap_radio = re.search("Radio Type\s+: (.+)", ap_data).group(1)
        #ap_metrics.append(ap_radio)

        ap_chutil = re.search("Channel Utilization\s+: (\S+)", ap_data).group(1)
        ap_chutil = int(ap_chutil[:-1])
        #ap_metrics.append(ap_chutil)

        ap_clients = re.search("Attached Clients\s+: (\S+)", ap_data).group(1)
        #ap_metrics.append(ap_clients)

        try:
            ap_changes = re.search("Channel Change Count\s+: (.+)", ap_data).group(1)
        except AttributeError:
            ap_changes = "-"
        #finally:
        #    ap_metrics.append(ap_changes)

        try:
            ap_lastchange = re.search("Last Channel Change Time\s+: (.+)", ap_data).group(1)
        except AttributeError:
            ap_lastchange = "-"
        #finally:
        #    ap_metrics.append(ap_lastchange)

        ap_metrics=(ap_name, ap_slot, ap_radio, ap_chutil, ap_clients, ap_changes, ap_lastchange)
        monitor_data.append(ap_metrics)

    monitor_data = sorted(monitor_data, key=lambda x: x[3], reverse=True)[0:send_top] #sort by ch.util
    try:
        post = requests.post(monitor_api, data=json.dumps(monitor_data), verify=False, timeout=2)
        print(monitor_ip, post.status_code)
    except requests.exceptions.ConnectTimeout:
        print(monitor_ip, "Timeout")
    except requests.exceptions.ConnectionError:
        print(monitor_ip, "Connection error")
    monitor_data = []
    time.sleep(5)

