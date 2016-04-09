from wigle2 import Wigle, WigleRatelimitExceeded

user = 'itbstudent'
password = 'p@SSW0RD'
ssid = 'eduroam'
maxnetwork = 100

def user_info():
    
    
    info = Wigle(user, password).get_user_info()
    if not info.get('success'):
        print('Unauthorized to get user info')
    else:
        print('User: %s' % info.get('userid', '<unknown>'))
        print('Donate data: %s' % info.get('donate', '<unknown>'))
        print('Joined on: %s' % info.get('joindate', '<unknown>'))
        print('Last logged in on: %s' % info.get('lastlogin', '<unknown>'))


def search():
    ssid = search('--ssid', dest='ssid', type=str,
                        help='SSID of the network')
    maxnetwork = max('--max', dest='max', type=int, default=20,
                        help='maximum number of networks to download')
    
    def notify_new_page(first):
        print("Downloading new page (records from %i)" % first)

    try:
        results = Wigle(user, password).search(
            ssid=ssid,
            on_new_page=notify_new_page,
            max_results=maxnetwork)

        for result in results:
            print("%(ssid)s, %(netid)s, %(trilat)s, %(trilong)s" % result)

    except WigleRatelimitExceeded:
            print("Cannot query Wigle - exceeded number of allowed requests")