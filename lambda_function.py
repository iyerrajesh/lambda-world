import os
import requests
from s3_handler import persist


SITE = os.environ['site']
EXPECTED = os.environ['expected']


def validate(res):
    '''Return False to trigger the canary

    Currently this simply checks whether the EXPECTED string is present.
    However, you could modify this to perform any number of arbitrary
    checks on the contents of SITE.
    '''
    return EXPECTED in res


def task(url, method='GET', payload=None):
    if payload is None:
        payload = {}
    resp = None
    try:
        resp = requests.request(method, url, params=payload, data=payload)
    except requests.exceptions.HTTPError:
        print(f"Error resp: {resp.status_code}")
        return None
    except requests.exceptions.Timeout:
        print('Error TimedOut')
        return None
    return resp.json()


def lambda_handler(event, context):
    ret = task(SITE)
    if ret:
        persist(SITE, ret)
