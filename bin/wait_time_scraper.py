"""Scrapes the wait times from the CA DMV's website and saves them to the
database.
"""
import logging

from sqlalchemy.orm import sessionmaker

import cadmv.dmv as dmv
import cadmv.queries as queries
import config


<<<<<<< HEAD
logger = logging.getLogger("cadmv.scraper")
=======
logger = logging.getLogger('dictionaryapi.session')
>>>>>>> 37a90c60cfe69cdeddc75e72d8376f51aed172c9


def main():
    """Run this with a cron job every 2 minutes or so"""
    wait_times = dmv.get_wait_times()

    Session = sessionmaker(bind=config.engine)
    session = Session()
    queries.create_wait_times(session, wait_times)


<<<<<<< HEAD
if __name__ == "__main__":
=======
if __name__ == '__main__':
>>>>>>> 37a90c60cfe69cdeddc75e72d8376f51aed172c9
    main()
