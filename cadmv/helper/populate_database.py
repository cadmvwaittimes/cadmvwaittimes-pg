"""Populates the database with the branches data"""
import sys

from sqlalchemy.orm import sessionmaker

import config
import offices
import cadmv.queries as queries


def prep_data():
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
        clean_office['name'] = office['name']
        clean_office['number'] = office['number']
        clean_office['region'] = int(office['region'])
        clean_office['hours'] = office['hours']
        clean_office['address'] = office['address']
        clean_office['latitude'] = float(office['latitude'])
        clean_office['longitude'] = float(office['longitude'])
        clean_office['nearby1'] = office['nearby1']
        clean_office['nearby2'] = office['nearby2']
        clean_office['nearby3'] = office['nearby3']
        clean_office['nearby4'] = office['nearby4']
        clean_office['nearby5'] = office['nearby5']

        cleaned.append(clean_office)

    return cleaned


def populate_branches_table(sessn, data=None):
    """Populates the branches table with all of the branches. If no data is
    passed, then data is pulled (and cleaned) from the offices module.
    Otherwise, the passed in data is used.
    """
    if data is None:
        data = prep_data()

    for datum in data:
        queries.create_new_branch(sessn, datum)


if __name__ == '__main__':
    Session = sessionmaker(bind=config.engine)
    session = Session()

    if len(sys.argv) < 2:
        populate_branches_table(session)
    else:
        populate_branches_table(session, sys.argv[1])
