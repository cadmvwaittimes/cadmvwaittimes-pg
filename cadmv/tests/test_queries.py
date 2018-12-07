"""Tests for the queries module"""
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .context import cadmv

from cadmv import models
from cadmv import queries


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


class GetQueriesTest(unittest.TestCase):
    """Tests the GET queries"""
    def setUp(self):
        """Setup an in-memory SQLite database"""
        self.engine = create_engine('sqlite://')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_get_branch_by_number(self):
        """Test that the queries.get_branch_by_number() function works"""
        # Populate the database
        branch = BRANCHES[0]
        b = models.Branch(**branch)
        self.session.add(b)
        self.session.commit()

        number = BRANCHES[0]['number']

        branch = queries.get_branch_by_number(self.session, number)
        self.assertEqual(number, branch.number)


if __name__ == '__main__':
    unittest.main()
