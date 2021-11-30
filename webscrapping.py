import requests
import re
from bs4 import BeautifulSoup
from requests.sessions import session
import time
import sys
import libtorrent as lt
session = lt.session()
session.listen_on(6881, 6891)
params = {
    'save_path': 'D:\Torrent Download',
    'storage_mode': lt.storage_mode_t(2),
    'paused': False,
    'auto_managed': True,
    'duplicate_is_error': True}

def get_torrent(magnet_link):
    #torrent_handle = session.add_torrent(params, magnet_link)
    torrent_handle = lt.add_magnet_uri(session, magnet_link, params)
    s = torrent_handle.status()
    while (not torrent_handle.is_seed()):
        time.sleep(1)
        print(torrent_handle.status().progress)
        s = torrent_handle.status()
        print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
        s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
        s.num_peers, s.state), end=' ')
        alerts = session.pop_alerts()
        for a in alerts:
            if a.category() & lt.alert.category_t.error_notification:
                print(a)

        sys.stdout.flush()

    time.sleep(1)
    print('Torrent Downloaded')
    return torrent_handle
               
ws = requests.get('https://eztv.ch')
soup = BeautifulSoup(ws.content, 'html.parser')
links_with_text = soup.find_all('a', attrs = {'href' : re.compile("^https")})
for link in links_with_text:
    print(link.get('href'))

        


        

