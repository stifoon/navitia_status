import requests

token='3b036afe-0110-4202-b9ed-99718476c2e0'

resp = requests.get('https://{}@api.navitia.io/v1/coverage/'.format(token))
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError(format(resp.status_code))

status_file = open('navitia_rt_status.csv', 'w')

total_network = 0
status_file.write('coverage;rt_count;proxy_count\n')
for region in resp.json()["regions"]:
    coverage_id = region['id']
    url = 'https://{}@api.navitia.io/v1/coverage/'.format(token) + coverage_id + '/status'
    coverage = requests.get(url)
    realtime_contributors_count= len(coverage.json()["status"]["realtime_contributors"] or [])
    proxies_count = 0
    for realtime_proxies in coverage.json()["status"]["realtime_proxies"]:
        proxies_count+= 1
    line_to_print = '{cov_id};{rt_count};{prox_count}'.format(cov_id=coverage_id, rt_count=realtime_contributors_count, prox_count=proxies_count)
    print line_to_print
    status_file.write(line_to_print + '\n')

