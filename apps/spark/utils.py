import re

def is_mobile_request(request):
    mobile_url = re.compile(r'.+/m/.+')
    return mobile_url.match(request.path) != None