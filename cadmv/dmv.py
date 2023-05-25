"""This modules defines the functions necessary to get data from the CA DMV"""
import datetime

import requests

from cadmv.helper import data


base_url = 'https://www.dmv.ca.gov/wasapp/webdata'
offices_json_url = base_url + '/foims_offices_min.json'
wait_times_url = base_url + '/output3.txt'


def get_offices_json(url: str = None, timeout: float = 1.0) -> list[dict]:
    """Makes a request to the offices_json_url URL and retrieves the CA DMV
    offices. timeout is set to 1 second because it seems like the DMV's site
    is slow to respond.

    Returns a list of dicts of offices with a lot of information including,
    but not limited to, name, address, hours, branch number, etc. See
    offices.py for an example of the response is returned.

    Args:
        url (str, optional): The URL to query. Defaults to None.
        timeout (float, optional): The length of the timeout. Defaults to 1.0.

    Raises:
        requests.exceptions.HTTPError: Raised if the response's status code is
        not 200 (OK)

    Returns:
        list[dict]: offices with a lot of information including, but not limited
        to, name, address, hours, branch number, etc. See offices.py for an
        example of the response is returned
    """
    if url is None:
        url = offices_json_url

    resp = requests.get(url, timeout=timeout)
    if not resp.ok:
        raise requests.exceptions.HTTPError()

    return resp.json()['foims_offices']['offices']


def get_wait_times(url: str = None, timeout: float = 1.0) -> list[dict]:
    """Makes a request to the wait_times_url URL and retrieves the wait times
    for each CA DMV office. timeout is to 1 second because it seems like the
    DMV's site is slow. The wait times request comes in as

    [
        568,0,10,
        ...
        538,0,23
    ]

    where the entries in a row correspond to branch number, appointments wait
    time (in minutes), and non-appoints wait time (in minutes), respectively.
    Returns a list of dicts of offices each with a dict of wait times for
    appointments and non-appointments of the form

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

    Args:
        url (str, optional): The URL to query. Defaults to None.
        timeout (float, optional): The length of the timeout. Defaults to 1.0.

    Raises:
        requests.exceptions.HTTPError: Raised if the response's status code is
        not 200 (OK)

    Returns:
        list[dict]: wait times for every branch in the format given above
    """
    if url is None:
        url = wait_times_url

    now = datetime.datetime.now()
    resp = requests.get(url, timeout=timeout)
    if not resp.ok:
        raise requests.exceptions.HTTPError

    text = resp.text.split('\r\n')[1:]
    del text[0] # remove the header

    wait_times = data.prep_wait_times_data(text, now)
    return wait_times
