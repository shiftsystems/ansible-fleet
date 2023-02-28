#!/usr/bin/python3
import json
import os
import requests
import sys
import time

# Fleet Connection info
fleet_base_url = os.environ.get('FLEET_BASE_URL')
auth_token = os.environ.get('AUTH_TOKEN')

# Loki Connection info
loki_base_url = os.environ.get('LOKI_BASE_URL')
loki_user = os.environ.get('LOKI_USER')
loki_password = os.environ.get('LOKI_PASSWORD')

print('successfully load environment variables')
print('grabbing host list from Fleet')
fleet_headers = {"Authorization": f'''Bearer {auth_token}'''}
host_list = requests.get(f'{fleet_base_url}/api/v1/fleet/hosts',headers=fleet_headers, verify=False)
print('successfully gathered host information')

#print(host_list.json())
print('grabbing host details from Fleet')
host_details = {}
for host in host_list.json()['hosts']:
    #print(f'''{host['display_name']}: id: {host['id']}''')
    host_data = requests.get(f'''{fleet_base_url}/api/v1/fleet/hosts/{host['id']}''',headers=fleet_headers,verify=False).json()
    vulns = {}
    policies = {}

    print(f'''gathering package and CVE information for {host['display_name']} from Fleet''')
    for package in host_data['host']['software']:
        if package['vulnerabilities']:
            #print(f'''{package['name']} vulnerabilities: {package['vulnerabilities']}''')
            for cve in package['vulnerabilities']:
                vulns.setdefault(cve['cve'],[]).append(package['name'])
    print(f'''successfully gathered package and CVE information for {host['display_name']} from Fleet''')
    #print(vulns)

    for vuln, packages in vulns.items():
        vulns[vuln] = ','.join(packages)
        #print(f'''{vuln}: {vulns[vuln]}''')

    for policy in host_data['host']['policies']:
        policies[policy['name'].replace(' ','_')] = policy['response']


    host_details[host['id']]= {
        "hostname": host_data['host']['hostname'],
        "vulnerabilities": vulns,
        "policies": policies,
    }
print('successfully gathered all data from Fleet')
#for host_id,host_data in host_details.items():
#    print(json.dumps(host_data))
#print(json.dumps(host_details))

# send data to loki
streams = []

for host_id,host_data in host_details.items():
    stream = {}
    values = []
    for policy,status in host_data['policies'].items():
        values.append([str(time.time_ns()),f'''policy={policy} status={status} '''])
    for cve, packages in host_data['vulnerabilities'].items():
        values.append([str(time.time_ns()),f'''cve={cve} packages={packages}'''])
    stream['stream'] = {"host": host_data['hostname'],"__name":"fleet_import"}
    stream['values'] = values
    streams.append(stream)

wrapper = {'streams': streams}
#print(json.dumps(wrapper))
loki_headers = {"Content-Type": "application/json"}
loki_result = requests.post(f'''{loki_base_url}/loki/api/v1/push''',data=json.dumps(wrapper),auth=(loki_user,loki_password),headers=loki_headers,verify=False)
if loki_result.status_code == 204:
    print('results successfully sent to Loki')
else:
    sys.exit(f'Sending info to loki failed Loki returned http status code {loki_result.status_code} expected 204')

#print(loki_result.text)