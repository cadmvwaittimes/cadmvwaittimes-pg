
import logging

from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

import config
from models import Branch, WaitTime


Session = sessionmaker(bind=config.engine)

logger = logging.getLogger('dictionaryapi.queries')


def create_new_branch(branch_info):
    """Creates a new word and definition in the database.

    :param branch_info word:  (dict) branch information in the form of
    {
        'address': "1330 E. First Street, Santa Ana, CA 92701",
        'hours': "0700-1700,0700-1700,0900-1700,0700-1700,0700-1700,n,n",
        'latitude': 33.745400,
        'longitude': -117.850600,
        'name': "Santa Ana",
        'nearby1': 698,
        'nearby2': 611,
        'nearby3': 628,
        'nearby4': 607,
        'nearby5': 607,
        'number': 542,
        'region': 7
    }
    """
    branch = Branch(**branch_info)
    with session_scope() as session:
        session.add(branch)


def update_branch(branch_info):
    """Updates the defintion of a word in the database

    :param branch_info word:  (dict) branch information in the form of
    {
        'address': "1330 E. First Street, Santa Ana, CA 92701",
        'hours': "0700-1700,0700-1700,0900-1700,0700-1700,0700-1700,n,n",
        'latitude': 33.745400,
        'longitude': -117.850600,
        'name': "Santa Ana",
        'nearby1': 698,
        'nearby2': 611,
        'nearby3': 628,
        'nearby4': 607,
        'nearby5': 607,
        'number': 542,
        'region': 7
    }
    Taken from https://stackoverflow.com/a/4540110
    NOTE: this could potentially be slow for a large number of entries.
    However, there's less than 200 CA DMVs so should be ok.
    """
    number = branch_info['number']
    with session_scope() as session:
        session.query(Branch).filter_by(number=number).\
            update(branch_info)


def get_branch_by_number(number):
    """Gets a branch by its number

    :param number:      (int) number of branch
    :returns branch:    first branch to match the number, or None if none
                        is found
    """
    session = Session()
    branch = None
    try:
        branch = session.query(Branch).filter_by(number=number).first()
    except:
        logger.error('An error occurred accessing the database', exc_info=True)
    finally:
        session.close()

    return branch


def get_branches_by_region(region):
    """Gets branches by region

    :param region:      (int) region number
    :returns branches:  all branches to match the region, or None if none
                        are found. NOTE: it's currently returning [] if
                        none are found...
    """
    session = Session()
    branches = None
    try:
        branches = session.query(Branch).filter_by(region=region).all()
    except:
        logger.error('An error occurred accessing the database', exc_info=True)
    finally:
        session.close()

    return branches


def is_branch_in_database(branch_num):
    """Determines if a branch exists in database.

    :param branch_num:  (int) branch number
    :return:            True if word is found in the database. Otherwise, False.
    """
    session = Session()
    does_exist = False
    try:
        does_exist = session.query(exists().where(
            Branch.number == branch_num)).scalar()
    except:
        logger.error('An error occurred accessing the database', exc_info=True)
    finally:
        session.close()

    return does_exist


def create_wait_time(wait_time):
    """Creates a new wait time entry in the database

    :param wait_time:   (dict) of a wait time of the form
    {
        'branch_id': 542,
        'appt': 15,
        'non_appt': 27,
        'timestamp': datetime.datetime(2018, 12, 6, 23, 22, 13, 859932)
    }
    """
    wt = WaitTime(**wait_time)
    with session_scope() as session:
        session.add(wt)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations.

    Taken from:

    https://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
    """
    session = Session()
    try:
        yield session
        session.commit()
    except:
        logger.error('An error occurred accessing the database', exc_info=True)
        session.rollback()
        raise
    finally:
        session.close()
