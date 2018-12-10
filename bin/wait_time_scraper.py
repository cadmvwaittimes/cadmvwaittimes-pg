"""Scrapes the wait times from the CA DMV's website and saves them to the
database.
"""
import logging

from sqlalchemy.orm import sessionmaker

import cadmv.dmv as dmv
import cadmv.queries as queries
import config


logger = logging.getLogger('dictionaryapi.session')


def main():
    """Run this with a cron job every 2 minutes or so"""
    wait_times = dmv.get_wait_times()

    Session = sessionmaker(bind=config.engine)
    session = Session()
    # NOTE: The below function does'n currently exist, but it will...
    queries.create_wait_times(session, wait_times)


if __name__ == '__main__':
    main()