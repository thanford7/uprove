import re
import requests

from bs4 import BeautifulSoup as bs
from requests import ConnectTimeout
from requests.exceptions import ProxyError, SSLError

ANONYMITY_CODES = {
    'N': 0,  # None
    'A': 1,  # Yes
    'H': 2  # High
}

PROXY_TARGET_COUNT = 10


def getProxies():
    proxyUrl = 'https://github.com/clarketm/proxy-list/blob/master/proxy-list.txt'
    r = requests.get(proxyUrl)
    proxySoup = bs(r.content, 'html.parser').find_all('td', {'class': 'blob-code blob-code-inner js-file-line'})
    proxies = []
    for proxyHtml in proxySoup:
        proxyRe = re.match('^(?P<address>[0-9\.:]+) [a-zA-Z]{2}-(?P<anonymity>[a-zA-Z])(?P<other>.*?)$', proxyHtml.getText())
        if not proxyRe:
            continue

        proxies.append({
            'address': proxyRe.group('address'),
            'anonymity': ANONYMITY_CODES[proxyRe.group('anonymity')],
            'isHttps': 'S' in proxyRe.group('other'),
            'isDifferentOutIP': '!' in proxyRe.group('other'),
            'isGooglePassed': '+' in proxyRe.group('other'),
        })

    return sorted(proxies, key=lambda p: (-p['isGooglePassed'], -p['anonymity'], -p['isHttps'], -p['isDifferentOutIP']))


def getWorkingProxies(proxies):
    goodProxies = []
    proxiesTried = 0
    while len(goodProxies) < PROXY_TARGET_COUNT and proxiesTried < len(proxies):
        proxy = proxies[proxiesTried]['address']
        print(f'Trying proxy <{proxy}>')
        try:
            r = requests.get(
                'https://www.indeed.com/',
                proxies={
                    'https': proxy,
                    'http': proxy
                },
                headers={
                    "referer": 'http://example.com',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'},
                timeout=2
            )
            if r.status_code >= 200 and r.status_code < 300:
                goodProxies.append(proxy)
                print(f'Found good proxy')
        except (ConnectTimeout, ProxyError, SSLError) as e:
            try:
                reason = e.args[0].reason.args[1]
            except:
                reason = e
            print(f'Failed: {reason}')
        proxiesTried += 1

    return goodProxies


proxies = getProxies()
goodProxies = getWorkingProxies(proxies)
print(goodProxies)
