"""Module that holds the database queries"""
from contextlib import contextmanager
import datetime
import logging

from sqlalchemy import update
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from cadmv.models import Branch, WaitTime
from cadmv.session import session_scope


# Session = sessionmaker(bind=config.engine)

logger = logging.getLogger('dictionaryapi.queries')


def create_new_branch(session, branch_info):
    """Creates a new DMV branch in the database.

    :param session:     SQLAlchemy session
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
    with session_scope(session) as sessn:
        sessn.add(branch)


def update_branch(session, branch_info):
    """Updates DMV branch in the database

    :param session:     SQLAlchemy session
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
    with session_scope(session) as sessn:
        sessn.query(Branch).filter_by(number=number).\
            update(branch_info)


def get_branch_by_number(session, number):
    """Gets a branch by its number

    :param session:     SQLAlchemy session
    :param number:      (int) number of branch
    :returns branch:    first branch to match the number, or None if none
                        is found
    """
    branch = None
    try:
        branch = session.query(Branch).filter_by(number=number).first()
    except:
        logger.error('An error occurred accessing the database', exc_info=True)
    finally:
        session.close()

    return branch


def get_branches_by_region(session, region):
    """Gets branches by region

    :param session:     SQLAlchemy session
    :param region:      (int) region number
    :returns branches:  all branches to match the region, or None if none
                        are found. NOTE: it's currently returning [] if
                        none are found...
    """
    branches = None
    try:
        branches = session.query(Branch).filter_by(region=region).all()
    except:
        logger.error('An error occurred accessing the database', exc_info=True)
    finally:
        session.close()

    return branches


def is_branch_in_database(session, branch_num):
    """Determines if a branch exists in database.

    :param branch_num:  (int) branch number
    :return:            True if word is found in the database. Otherwise, False.
    """
    does_exist = False
    try:
        does_exist = session.query(exists().where(
            Branch.number == branch_num)).scalar()
    except:
        logger.error('An error occurred accessing the database', exc_info=True)
    finally:
        session.close()

    return does_exist


def create_wait_time(session, wait_time):
    """Creates a new wait time entry in the database

    :param session:     SQLAlchemy session
    :param wait_time:   (dict) of a wait time of the form
    {
        'branch_id': 542,
        'appt': 15,
        'non_appt': 27,
        'timestamp': datetime.datetime(2018, 12, 6, 23, 22, 13, 859932)
    }
    """
    wt = WaitTime(**wait_time)
    with session_scope(session) as sessn:
        sessn.add(wt)


def create_wait_times(session, wait_times):
    """Creates new wait time entries in the database en masse

    :param session:     SQLAlchemy session
    :param wait_times:  (list) of a wait times of the form
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
    wts = [WaitTime(**wt) for wt in wait_times]

    with session_scope(session) as sessn:
        sessn.add_all(wts)


def get_wait_time_by_number(session, branch_num):
    """Gets the wait times for a particular DMV branch

    :param session:     SQLAlchemy session
    :param branch_num:  (int) branch number
    :return:            (list) of all wait times for the desired branch if
                        there are any in the database. Otherwise, returns
                        None
    """
    wait_times = None
    try:
        wait_times = session.query(WaitTime).\
            filter_by(branch_id=branch_num).first()
    except:
        logger.error('An error occurred accessing the database', exc_info=True)
    finally:
        session.close()

    return wait_times


def get_wait_time_by_date(session, date):
    """Gets the wait times for a particular DMV branch

    :param session: SQLAlchemy session
    :param date:    (datetime) date
    :return:        (list) of all wait times for the desired date if there
                    are any in the database. Otherwise, returns an empty
                    list
    """
    wait_times = None
    try:
        wait_times = session.query(WaitTime).\
            filter_by(timestamp=date).all()
    except:
        logger.error('An error occurred accessing the database', exc_info=True)
    finally:
        session.close()

    return wait_times


def get_wait_times_by_region(session, region):
    """Gets the wait times for a particular DMV branch

    :param session:     SQLAlchemy session
    :param branch_num:  (int) branch number
    :return:            (list) of all wait times and associated branches for
                        the desired region if there are any in the database.
                        Otherwise, returns an empty list
    """
    # NOTE: this is returning a tuple of pairs of wait times and branches which
    # is NOT what I want. I want to return only a list of wait times. So, this
    # is a work in progress
    wait_times = None
    try:
        query = session.query(WaitTime, Branch)
        wait_times = query.filter(Branch.region==region)\
                          .filter(Branch.number==WaitTime.branch_id).all()
    except:
        logger.error('An error occurred accessing the database', exc_info=True)
    finally:
        session.close()

    return wait_times
