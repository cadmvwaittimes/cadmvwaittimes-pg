"""Helper functions for working with/cleaning data"""
import ast
import re
from xml.etree.ElementTree import Element

from defusedxml.ElementTree import fromstring

import offices


def prep_branches_data():
    """Prepares the data for inserting into the database. Currently, the data
    has a lot of information that isn't necessary. An example of a cleaned
    entry is:

    {
        "name": "South Lake Tahoe",
        "number": 538,
        "region": "3",
        "hours": "0800-1700,0800-1700,0900-1700,0800-1700,0800-1700,n,n"
        "address": "3344 B Lake Tahoe Boulevard, South Lake Tahoe, CA 96150",
        "latitude": 38.945748,
        "longitude": -119.969890,
        "nearby1": 0,
        "nearby2": 0,
        "nearby3": 0,
        "nearby4": 0,
        "nearby5": 0
    }

    :return cleaned:    (list) cleaned data with only the attributes that are
                        found in the model
    """
    cleaned = []

    for office in offices.original_offices:
        clean_office = {}
        clean_office["name"] = office["name"]
        clean_office["number"] = office["number"]
        clean_office["region"] = int(office["region"])
        clean_office["hours"] = office["hours"]
        clean_office["address"] = office["address"]
        clean_office["latitude"] = float(office["latitude"])
        clean_office["longitude"] = float(office["longitude"])
        clean_office["nearby1"] = office["nearby1"]
        clean_office["nearby2"] = office["nearby2"]
        clean_office["nearby3"] = office["nearby3"]
        clean_office["nearby4"] = office["nearby4"]
        clean_office["nearby5"] = office["nearby5"]

        cleaned.append(clean_office)

    return cleaned


def prep_wait_times_data(data, timestamp):
    """Prepares the wait times data taken from the CA DMV's website to be
    entered into the database. The wait times request comes in as

    [
        568,0,10,
        ...
        538,0,23
    ]

    where the entries in a row correspond to branch number, appointments wait
    time (in minutes), and non-appoints wait time (in minutes), respectively.
    The data is transformed to be of the form

    [
        {
            'branch_id': 568,
            'appt': 0,
            'non_appt': 10,
            'timestamp': datetime.datetime(2018, 12, 6, 23, 22, 13, 859932)
        },
        ...
        {
            'branch_id': 538,
            'appt': 0,
            'non_appt': 23,
            'timestamp': datetime.datetime(2018, 12, 6, 23, 22, 13, 859932)
        }
    ]

    Note that the timestamps all have the same time because they are all sourced
    at the same time.
    """
    wait_times = [
        {
            "branch_id": wt[0],
            "appt": wt[1],
            "non_appt": wt[2],
            "timestamp": timestamp,
        }
        for wt in data
    ]

    return wait_times


def split_response(response: str) -> tuple:
    """
    Splits the response from the DMV into its constituent parts of an XML tree
    and a list of tuples of ints.
    """
    pattern = r"\d+,\d+,\d+"
    index = re.search(pattern, response).start()

    return (
        text_to_xml(response[:index]),
        parse_wait_time_list(response[index:].split("\r\n")),
    )


def text_to_xml(text: str) -> Element:
    """
    Takes a string of (an ill-formed, i.e., no root in this case) an XML tree
    and returns an Element object with the root `<cadmv>` added.
    """
    first_line = len(text.split("\r\n")[0])
    tree = fromstring(f"<cadmv>{text[first_line:]}</cadmv>")
    return tree


def parse_wait_time_list(wt_string: list) -> list:
    """
    Takes a list of strings and transforms it to a list of tuples of ints. For
    example,
    Input:
    [
        '658,0,0,',
        '697,0,0,',
        '648,0,0,',
        '630,0,0,',
        '569,0,0,',
        '571,0,0,',
        '610,0,0,',
        '664,0,0,'
    ]

    is transformed to

    [
        (658, 0, 0),
        (697, 0, 0),
        (648, 0, 0),
        (630, 0, 0),
        (569, 0, 0),
        (571, 0, 0),
        (610, 0, 0),
        (664, 0, 0)
    ]
    """
    return [ast.literal_eval(wt) for wt in wt_string]
