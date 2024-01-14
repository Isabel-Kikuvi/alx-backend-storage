#!/usr/bin/env python3
""" In this tasks, we will implement a get_page function (prototype:
    def get_page(url: str) -> str:). The core of the function is very simple.
    It uses the requests module to obtain the HTML content of a particular
    URL and returns it.
"""


import redis
import requests
from functools import wraps

r = redis.Redis()


def url_access_count(method):
    """get_page function decorator"""
    @wraps(method)
    def wrapper(url):
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        key_count = "count:" + url
        html_content = method(url)

        r.incr(key_count)
        r.set(key, html_content, ex=10)
        r.expire(key, 10)
        return html_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """Obtains the HTML content"""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
