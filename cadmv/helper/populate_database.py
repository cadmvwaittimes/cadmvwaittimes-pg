"""Populates the database with the branches data"""
import sys

from sqlalchemy.orm import sessionmaker

import config
import cadmv.helper.data
import cadmv.queries as queries


def populate_branches_table(sessn, data=None):
    """Populates the branches table with all of the branches. If no data is
    passed, then data is pulled (and cleaned) from the offices module.
    Otherwise, the passed in data is used.
    """
    if data is None:
        data = cadmv.helper.data.prep_branches_data()

    for datum in data:
        queries.create_new_branch(sessn, datum)


if __name__ == '__main__':
    Session = sessionmaker(bind=config.engine)
    session = Session()

    if len(sys.argv) < 2:
        populate_branches_table(session)
    else:
        populate_branches_table(session, sys.argv[1])
