# coding=utf-8
from __future__ import unicode_literals
import requests
from lxml import html

URL = 'http://146.185.169.28'
TEST = '/doorhan_test/'
LOGIN = PASS = 'Anders'


def remove_specific_order(order_name):
    s = requests.session()

    payload_login = {'LoginForm[username]': LOGIN, 'LoginForm[password]': PASS, 'LoginForm[rememberMe]': '0'}
    url_login = ''.join([URL, TEST, 'site/login'])
    s.post(url_login, data=payload_login)

    payload_order = {
        'OrderModel[number]': order_name,
        'OrderModel[constructor_id]': '',
        'OrderModel[year]': '',
        'OrderModel[dateField]': 'calculationDate',
        'OrderModel[period]': '5'
    }
    url_order = ''.join([URL, TEST, 'constructor/order/index?'])
    r = s.get(url_order, data=payload_order)

    tree = html.document_fromstring(r.content)
    link1 = tree.xpath('//a[.="%s"]' % order_name)[0].attrib['href']
    order_id = link1.split('/')[-1]

    r = s.get(''.join([URL, link1]))
    tree = html.document_fromstring(r.content)
    link2 = tree.cssselect('a[href*="/readProduct/id/"]')[0].attrib['href']
    # _id = link2.split('/readProduct/id/')[-1].split('/')[0]

    # print "link1 = %s" % link1
    # print "order_id = %s" % order_id
    # print "_id = %s" % _id
    # print "link2 = %s" % link2

    mark_to_delete_product_link = ''.join([URL, link2]).replace('readProduct', 'markToDeleteProduct')
    s.get(mark_to_delete_product_link)

    save_order_link = ''.join([URL, link1]).replace('update', 'saveOrder')
    s.get(save_order_link)

    payload_delete = {
        'yw0_c0_all': '1',
        'ids[]': order_id
    }
    url_delete = ''.join([URL, TEST, 'constructor/order/delete'])
    r = s.post(url_delete, data=payload_delete)
    content = unicode(r.content, 'utf-8')

    for err in ['Error', 'error']:
        assert err not in content


if __name__ == '__main__':
    try:
        remove_specific_order('MSВДВ096288')
    except IndexError:
        print 'there is no order with that name.'
