"""Tests for the queries module"""
import copy
import unittest

from sqlalchemy import create_engine, MetaData
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
        """Test that DMV branch is upated"""
        new_address = '123 Fake St., Springfield, OH 45503'
        b = copy.deepcopy(BRANCHES[0])
        b['address'] = new_address
        queries.update_branch(self.session, b)
        branch = self.session.query(models.Branch).\
            filter_by(number=b['number']).first()
        self.session.close()

        self.assertEqual(branch.address, new_address)


class CreateWaitTimeQueriesTest(unittest.TestCase):
    """Tests the CREATE WaitTime queries"""
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


if __name__ == '__main__':
    unittest.main()
