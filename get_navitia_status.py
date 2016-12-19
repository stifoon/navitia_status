# coding: utf8
import ConfigParser
import requests

config = ConfigParser.ConfigParser()
config.readfp(open('get_navitia_status.ini'))
my_token= config.get('DEFAULT','token')

resp = requests.get('https://{}@api.navitia.io/v1/coverage/'.format(my_token))


if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError(format(resp.status_code))

status_file = open('navitia_rt_status.csv', 'w')
head_line= u'coverage;is_open_data;rt_count;proxy_count;networks\n'
status_file.write(head_line.encode('utf-8'))

total_network = 0
for region in resp.json()["regions"]:
    #request for one coverage
    coverage_id = region['id']
    print coverage_id
    url = 'https://{}@api.navitia.io/v1/coverage/'.format(my_token) + coverage_id + '/status'
    response = requests.get(url)

    #reading the response 
    is_open_data= response.json()['status']['is_open_data']

    #any Traffic_report feeders ?
    realtime_contributors_count= len(response.json()['status']['realtime_contributors'] or [])

    #any proxy departures feeders ?
    proxies_count = 0
    for realtime_proxies in response.json()['status']['realtime_proxies']:
        proxies_count+= 1

    #networks
    networks = u''
    url = 'https://{}@api.navitia.io/v1/coverage/'.format(my_token) + coverage_id + '/networks'
    response = requests.get(url)
    for network in response.json()['networks']:
        networks = networks + network['name'] + '\n'
    networks = '"' + networks.encode('utf-8') + '"'

    #write line
    line_to_print = '{cov_id};{is_od};{rt_count};{prox_count};{netwk}'.format(cov_id=coverage_id, is_od=is_open_data, rt_count=realtime_contributors_count, prox_count=proxies_count, netwk=networks)
    line_to_print = line_to_print + '\n'
    status_file.write(line_to_print)

