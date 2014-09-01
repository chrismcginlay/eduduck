# video/utils.py

import re

from urlparse import parse_qs, urlparse

def get_youtube_id_from_url(url):
    """Extract the video ID code from various youtube URLs"""

    yt_url = urlparse(url)
    if not(yt_url.netloc == r'youtu.be' or yt_url.netloc == r'www.youtube.com'):
        return None
    if yt_url.netloc == r'youtu.be':
        id = yt_url.path[1:]
        if not len(id) == 11:
            return None
        else:
            return id

    targ = re.match(r'^/embed/|/v/|/e/', yt_url.path)
    if targ:
        id_start = targ.end()
        id = targ.string[id_start:]
        if not len(id) == 11:
            return None
        else:
            return id 
    parameters = parse_qs(yt_url.query)    
    try:
        id = parameters['v'][0]
    except KeyError:
        return None
    if not len(id) == 11:
        return None
    else:
        return id

