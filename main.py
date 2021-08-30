import requests


class Proxy:
    def __init__(self, json: dict) -> None:
        self.ip = json['ip']
        self.port = json['port']
        self.anonymityLevel = json['anonymityLevel']
        self.country = json['country']
        self.latency = json['latency']
        self.protocols = json['protocols']

    def __repr__(self):
        return f"Proxy: {self.ip}:{self.port}\nCountry: {self.country}\nLatency: {self.latency}\nProtocols: {','.join(self.protocols)}"


class ProxyGetter:
    URL = "https://proxylist.geonode.com/api/proxy-list"
    TEST_URL = "https://ifconfig.me/ip"
    DEF_OPTIONS = {
        'limit': '50',
        'page': '1',
        'sort_by': 'speed',
        'sort_type': 'asc',
        # 'country': 'IN',
        'speed': 'fast',
        # 'protocols': 'https',
        # 'anonymityLevel': 'elite',
        # 'anonymityLevel': 'anonymous',
        # 'anonymityLevel': 'transparent'
    }

    def __init__(self, options: dict = None) -> None:
        self.OPTIONS = options if options else self.DEF_OPTIONS

    def get(self):
        data = requests.get(self.URL, params=self.OPTIONS).json()
        print(f"Found {data['total']} proxies!")
        proxies = list()
        for proxy in data['data']:
            proxies.append(Proxy(proxy))
        return proxies

    def test(self, proxy: Proxy, timeout: int = 5):
        try:
            response = requests.get(self.TEST_URL, timeout=timeout, proxies={
                "https": f"{proxy.protocols[0]}://{proxy.ip}:{proxy.port}"}).content.decode()
        except:
            return "Not OK"
        return "OK" if response == proxy.ip else "Not OK"


if __name__ == '__main__':
    proxy = ProxyGetter()
    proxies = proxy.get()
    print('Testing top 10...')
    for pr in proxies[:10]:
        print(pr)
        print(f"Result: {proxy.test(pr)}\n")
