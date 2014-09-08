import requests
import os
from basetest import URL, LOGIN, PASS


def check_csv_file(order_specification_url):
    csv_file_name = 'specification.csv'
    payload = {'LoginForm[username]': LOGIN, 'LoginForm[password]': PASS, 'LoginForm[rememberMe]': '0'}
    url = ''.join([URL, 'site/login'])
    csv_url = ''.join([URL, 'constructor/order/specificationToCsv'])
    s = requests.session()
    s.post(url, data=payload)
    s.get(order_specification_url)

    with open(csv_file_name, 'wb') as handle:
        response = s.get(csv_url, stream=True)

        if not response.ok:
            print 'Something went wrong'

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
    s.close()
    csv_is_not_empty = os.path.getsize(csv_file_name) > 0
    os.remove(csv_file_name)
    return csv_is_not_empty