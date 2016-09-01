import os
import requests
import yaml
from subprocess import call, DEVNULL

work_dir = os.path.dirname(os.path.abspath(__file__))
requests.packages.urllib3.disable_warnings()
with open(os.path.join(work_dir, 'test_http.yml')) as file:
    settings = yaml.load(file.read())

hosts = settings['hosts']


def output(a='', b='', c=''):
    print('{:>4} {:<30} {}'.format(a,b,c))


def debug(msg):
    if settings['debug']:
        print('DEBUG: ' + msg)


def clearcache():
    if settings['clear_dns_cache']:
        debug('clearing dns cache')
        call('ipconfig /flushdns', stdout=DEVNULL, stderr=DEVNULL)


print('One interation contains http requests to the following hosts:')
print('\n'.join(hosts),end='\n\n')


def poll():
    key = int(input('Enter number of iterations. 0 to quit: '))
    if key == 0:
        raise StopIteration
    else:
        print()
        output('CODE','LINK','CONTENT')
        print('-'*60)

        for i in range(key):
            clearcache()
            for url in hosts:
                try:
                    session = requests.get(url, verify=False)
                    output(session.status_code,url,session.text.rstrip()[0:24])
                except requests.exceptions.ConnectionError:
                        output('',url,'connection refused')
            print()
        print()

while True:
    try:
        poll()
    except ValueError:
        print('Please enter an integer.')
    except (StopIteration, KeyboardInterrupt):
        print('Bye.')
        break
    except Exception as e:
        print('Unknown error:', e)
        break
