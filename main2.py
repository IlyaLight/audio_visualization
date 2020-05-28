import re

def domain_name(url):
    return re.search(r'(?!w{1,}\.)(\w+\.?)([a-zA-Z])(?=\.)', url)[0]

print(domain_name("http://google.com"))