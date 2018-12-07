"""This modules defines the functions necessary to get data from the CA DMV"""
import datetime

import requests


base_url = 'https://www.dmv.ca.gov/wasapp/webdata'
offices_json_url = base_url + '/foims_offices_min.json'
wait_times_url = base_url + '/output3.txt'


def get_offices_json(url=None, timeout=1):
    """
    Makes a request to the offices_json_url URL and retrieves the CA DMV
    offices. timeout is set to 1 second because it seems like the DMV's site
    is slow to respond.

    Returns a list of dicts of offices with a lot of information including,
    but not limited to, name, address, hours, branch number, etc. See
    offices.py for an example of the response is returned.
    """
    if url is None:
        url = offices_json_url

    resp = requests.get(url, timeout=timeout)
    if not resp.ok:
        raise requests.exceptions.HTTPError

    return resp.json()['foims_offices']['offices']


def get_wait_times(url=None, timeout=1):
    """
    Makes a request to the wait_times_url URL and retrieves the wait times
    for each CA DMV office. timeout is to 1 second because it seems like the
    DMV's site is slow.

    Returns a list of dicts of offices each with a dict of wait times for
    appointments and non-appointments.
    [
        {
            'branch_id': 542,
            'appt': 15,
            'non_appt': 27,
            'timestamp': datetime.datetime(2018, 12, 6, 23, 22, 13, 859932)
        },
        ...
        {
            'branch_id': 537,
            'appt': 26,
            'non_appt': 47,
            'timestamp': datetime.datetime(2018, 12, 6, 23, 22, 13, 859932)
        }
    ]
    """
    if url is None:
        url = wait_times_url

    now = datetime.datetime.utcnow()
    resp = requests.get(url, timeout=timeout)
    if not resp.ok:
        raise requests.exceptions.HTTPError

    text = resp.text.split('\r\n')
    del text[0] # remove the header

    # NOTE: Let's let the database save the timestamps
    # utcnow = str(datetime.datetime.utcnow())
    wait_times = []

    for wt in text:
        wt = wt.split(',')
        wait_time = {
            'branch_id': int(wt[0]),
            'appt': int(wt[1]),
            'non_appt': int(wt[2]),
            'timestamp': now
        }
        wait_times.append(wait_time)

    return wait_times
