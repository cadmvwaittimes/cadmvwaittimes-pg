"""Tests for the queries module"""
import copy
import datetime
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import cadmv.models as models
import cadmv.queries as queries


# Data to use for mock databases
BRANCHES = [
    {
        'address': '1330 E. First Street, Santa Ana, CA 92701',
        'hours': '0700-1700,0700-1700,0900-1700,0700-1700,0700-1700,n,n',
        'latitude': 33.745400,
        'longitude': -117.850600,
        'name': 'Santa Ana',
        'nearby1': 698,
        'nearby2': 611,
        'nearby3': 628,
        'nearby4': 607,
        'nearby5': 607,
        'number': 542,
        'region': 7
    },
    {
        'address': '903 W C St, Alturas, CA 96101',
        'hours': '0800-1700,0800-1700,0900-1700,0800-1700,0800-1700,n,n',
        'latitude': 41.491962,
        'longitude': -120.549754,
        'name': 'Alturas',
        'nearby1': 643,
        'nearby2': 553,
        'nearby3': 531,
        'nearby4': 639,
        'nearby5': 544,
        'number': 537,
        'region': 1
    }
]

WAIT_TIMES = [
    {
        'branch_id': 542,
        'appt': 15,
        'non_appt': 27,
        'timestamp': datetime.datetime(2018, 12, 6, 23, 22, 13, 859932)
    },
    {
        'branch_id': 537,
        'appt': 26,
        'non_appt': 47,
        'timestamp': datetime.datetime(2018, 12, 6, 23, 22, 13, 859932)
    }
]


class GetBranchQueriesTest(unittest.TestCase):
    """Tests the GET Branch queries"""

    def setUp(self):
        """Setup an in-memory SQLite database"""
        self.engine = create_engine('sqlite://')
        models.Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        # Populate the database
        branch = BRANCHES[0]
        b = models.Branch(**branch)
        self.session.add(b)
        self.session.commit()

    def tearDown(self):
        """Close the session after each test"""
        self.session.close()

    def test_get_branch_by_number_success(self):
        """Test that the queries.get_branch_by_number() function works"""
        number = BRANCHES[0]['number']

        branch = queries.get_branch_by_number(self.session, number)
        self.assertEqual(number, branch.number)

    def test_get_branch_by_number_fail(self):
        """Test that the queries.get_branch_by_number() function returns None
        when a branch requested for a number that doesn't exist.
        """
        branch = queries.get_branch_by_number(self.session, 9999999)
        self.assertIsNone(branch)

    def test_get_branches_by_region_success(self):
        """Test that the queries.get_branches_by_region() function works when
        given a correct region. I.e., at least one branch should be returned
        in a list.
        """
        region = BRANCHES[0]['region']

        branch = queries.get_branches_by_region(self.session, region)
        self.assertEqual(region, branch[0].region)

    def test_get_branches_by_region_fail(self):
        """Test that the queries.et_branches_by_region() function fails when
        given an incorrect region. I.e., an empty list should be returned.
        """
        region = 99999

        branch = queries.get_branches_by_region(self.session, region)
        self.assertEqual(0, len(branch))


class CreateBranchQueriesTest(unittest.TestCase):
    """Tests the CREATE Branch queries"""

    def setUp(self):
        """Setup an in-memory SQLite database"""
        self.engine = create_engine('sqlite://')
        models.Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_create_new_branch(self):
        """Test that a new DMV branch is created"""
        branch = BRANCHES[0]
        queries.create_new_branch(self.session, branch)
        b = self.session.query(models.Branch).\
            filter_by(number=branch['number']).first()
        self.session.close()

        self.assertIsInstance(b, models.Branch)


class UpdateBranchQueriesTest(unittest.TestCase):
    """Tests the UPDATE Branch queries"""

    def setUp(self):
        """Setup an in-memory SQLite database and create a branch"""
        self.engine = create_engine('sqlite://')
        models.Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Create a branch and add it to the DB
        b = BRANCHES[0]
        branch = models.Branch(**b)
        self.session.add(branch)
        self.session.commit()

    def test_update_new_branch(self):
        """Test that DMV branch is updated"""
        new_address = '123 Fake St., Springfield, OH 45503'
        b = copy.deepcopy(BRANCHES[0])
        b['address'] = new_address
        queries.update_branch(self.session, b)
        branch = self.session.query(models.Branch).\
            filter_by(number=b['number']).first()
        self.session.close()

        self.assertEqual(branch.address, new_address)


class IsBranchInDatabaseQueriesTest(unittest.TestCase):
    """Tests the is_branch_in_database function"""

    def setUp(self):
        """Setup an in-memory SQLite database"""
        self.engine = create_engine('sqlite://')
        models.Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Create a branch and add it to the DB
        b = BRANCHES[0]
        branch = models.Branch(**b)
        self.session.add(branch)
        self.session.commit()

    def tearDown(self):
        """Close the connection to the database after each test"""
        self.session.close()

    def test_is_branch_in_database_true(self):
        """Test that a branch that is in the database returns True"""
        branch_num = BRANCHES[0]['number']
        is_in_db = queries.is_branch_in_database(self.session, branch_num)
        self.assertTrue(is_in_db)

    def test_is_branch_in_database_false(self):
        """Test that a branch that is in the database returns True"""
        branch_num = 999999999
        is_in_db = queries.is_branch_in_database(self.session, branch_num)
        self.assertFalse(is_in_db)


class CreateWaitNewTimeQueriesTest(unittest.TestCase):
    """Tests the CREATE WaitTime queries"""

    def setUp(self):
        """Setup an in-memory SQLite database"""
        self.engine = create_engine('sqlite://')
        models.Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        """Close the connection to the database after each test"""
        self.session.close()

    def test_create_new_wait_times(self):
        """Test that new wait time entries are created"""
        queries.create_wait_times(self.session, WAIT_TIMES)
        wt = self.session.query(models.WaitTime).filter_by().all()

        self.assertEqual(len(wt), 2)


class CreateWaitNewTimesQueriesTest(unittest.TestCase):
    """Tests the CREATE WaitTime en masse queries"""

    def setUp(self):
        """Setup an in-memory SQLite database"""
        self.engine = create_engine('sqlite://')
        models.Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_create_new_wait_times(self):
        """Test that new wait times are created for a DMV branch"""
        queries.create_wait_times(self.session, WAIT_TIMES)
        wts = self.session.query(models.WaitTime).all()
        self.session.close()

        self.assertEqual(len(wts), 2)


class GetWaitTimeByNumberQueriesTest(unittest.TestCase):
    """Tests the GET WaitTime queries by branch number"""

    def setUp(self):
        """Setup an in-memory SQLite database"""
        self.engine = create_engine('sqlite://')
        models.Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        """Close the session after the test is run"""
        self.session.close()

    def test_get_wait_time_by_number_success(self):
        """Test that a new DMV branch is created"""
        # Create a wait time and add it to the DB
        w = WAIT_TIMES[0]
        wait_time = models.WaitTime(**w)
        self.session.add(wait_time)
        self.session.commit()

        wt = queries.get_wait_time_by_number(
            self.session, WAIT_TIMES[0]['branch_id'])

        self.assertIsInstance(wt, models.WaitTime)

    def test_get_wait_time_by_number_fail(self):
        """Test that a new DMV branch is created"""
        wt = queries.get_wait_time_by_number(self.session, 99999999)

        self.assertIsNone(wt, models.WaitTime)


class GetWaitTimeByDateQueriesTest(unittest.TestCase):
    """Tests the GET WaitTime queries by date"""

    def setUp(self):
        """Setup an in-memory SQLite database"""
        self.engine = create_engine('sqlite://')
        models.Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Create a wait time and add it to the DB
        w1 = WAIT_TIMES[0]
        w2 = WAIT_TIMES[1]
        wait_times = [models.WaitTime(**w1), models.WaitTime(**w2)]
        self.session.add_all(wait_times)
        self.session.commit()

    def tearDown(self):
        """Close the session after the test is run"""
        self.session.close()

    def test_get_wait_time_by_date_success(self):
        """Test that wait times are received for a given date"""
        date = datetime.datetime(2018, 12, 6, 23, 22, 13, 859932)

        wt = queries.get_wait_time_by_date(self.session, date)

        self.assertEqual(len(wt), 2)

    def test_get_wait_time_by_date_fail(self):
        """Test that wait times are not received for a given, incorrect date"""
        date = datetime.datetime(2010, 12, 6, 23, 22, 13, 859932)

        wt = queries.get_wait_time_by_date(self.session, date)

        self.assertEqual(len(wt), 0)


class GetWaitTimesByRegionQueriesTest(unittest.TestCase):
    """Tests the GET WaitTimes queries by region"""

    def setUp(self):
        """Setup an in-memory SQLite database"""
        self.engine = create_engine('sqlite://')
        models.Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Create entries for branches in the database
        branches = [models.Branch(**b) for b in BRANCHES]
        self.session.add_all(branches)

    def tearDown(self):
        """Close the session after the test is run"""
        self.session.close()

    def test_get_wait_times_by_region_success(self):
        """Test that wait times are retrieved for a certain region"""
        # Create a wait time and add it to the DB
        w = WAIT_TIMES[0]
        wait_time = models.WaitTime(**w)
        self.session.add(wait_time)
        self.session.commit()

        wt = queries.get_wait_times_by_region(
            self.session, BRANCHES[0]['region'])

        self.assertEqual(len(wt), 1)

    def test_get_wait_times_by_region_fail(self):
        """Test that a wait times are not retrieved for a non-existent
        region
        """
        wt = queries.get_wait_times_by_region(self.session, 99999999)

        self.assertEqual(len(wt), 0)


if __name__ == '__main__':
    unittest.main()
