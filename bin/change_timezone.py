"""Changes the time stamp of each entry in the database. USE WITH CAUTION

Takes in one argument: the time delta in hours. Put the argument in
quotations. For example,

$ python change_timezone.py "-8"

to get negative shifts.
"""
import argparse
import datetime

from sqlalchemy.orm import sessionmaker

import cadmv.models
import cadmv.session
import config


Session = sessionmaker(bind=config.engine)
session = Session()

<<<<<<< HEAD
description = "Script to modify the time stamps of each data point." "USE WITH CAUTION!"
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-d", action="store", dest="diff", type=int)

if __name__ == "__main__":
=======
description = ('Script to modify the time stamps of each data point.'
               'USE WITH CAUTION!')
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-d', action='store', dest='diff', type=int)

if __name__ == '__main__':
>>>>>>> 37a90c60cfe69cdeddc75e72d8376f51aed172c9
    args = parser.parse_args()
    diff = args.diff
    delta = datetime.timedelta(hours=diff)

    # Get every wait time data point
<<<<<<< HEAD
    print("Gathering data...")
    wait_times = session.query(cadmv.models.WaitTime).all()
    # Apply time delta
    print(f"Applying time change by {diff} hours")
=======
    print('Gathering data...')
    wait_times = session.query(cadmv.models.WaitTime).all()
    # Apply time delta
    print(f'Applying time change by {diff} hours')
>>>>>>> 37a90c60cfe69cdeddc75e72d8376f51aed172c9
    for wt in wait_times:
        wt.timestamp += delta

    # Commit the changes
<<<<<<< HEAD
    print("Adding modified data to database...")
    session.add_all(wait_times)
    print("Committing changes...")
    session.commit()
    session.close()
    print("Done")
=======
    print('Adding modified data to database...')
    session.add_all(wait_times)
    print('Committing changes...')
    session.commit()
    session.close()
    print('Done')
>>>>>>> 37a90c60cfe69cdeddc75e72d8376f51aed172c9
