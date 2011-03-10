
import urllib2

def url2qr(url, size=150):
    API = 'https://chart.googleapis.com/chart?chs=%dx%d&cht=qr&chl=%s&chld=L|1'
    
    return API % (size, size, urllib2.quote(url))