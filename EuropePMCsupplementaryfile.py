from requests_html import HTMLSession
import pandas as pd
from itertools import chain

def baseurl(url):
    s = HTMLSession()
    r = s.get(url)
    cont = r.html.find('a', containing='PMCxxxx')
    links = []
    for url in cont:
        h = 'http://europepmc.org/ftp/suppl/OA/' + url.find('a', first=True).attrs['href']
        links.append(h)
    return links


def getsupplementaryurls(res):
    s = HTMLSession()
    r = s.get(res)
    cont = r.html.find('a', containing='.zip')
    supplementaryfile = []
    for suppurl in cont:
        surl = res + suppurl.find('a', first=True).attrs['href']
        supplementaryfile.append(surl)
    return supplementaryfile

mainlist = []
urllist = baseurl('http://europepmc.org/ftp/suppl/OA/')[0:2]
for res in urllist:
    mainlist.append(getsupplementaryurls(res))
    print('getting url:', res)
    
df = pd.DataFrame(list(chain.from_iterable(mainlist)))
df.to_csv('supplementaryfiles.csv', index=False)
print('Downloas finished')