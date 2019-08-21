import requests

def get_or_raise(url):
    r = requests.get(url)
    if not r.status_code==200:
        raise RuntimeError("error getting data from AWS")
    
    return r.text


def get_ipv4():
    url = "http://169.254.169.254/latest/meta-data/public-ipv4"
    return get_or_raise(url)

def get_ipv6():
    url1 = "http://169.254.169.254/latest/meta-data/network/interfaces/macs/"
    url2 = "http://169.254.169.254/latest/meta-data/network/interfaces/macs/__mac__/ipv6s"
    
    mac = get_or_raise(url1)
    return get_or_raise(url2.replace("__mac__", mac))
    
