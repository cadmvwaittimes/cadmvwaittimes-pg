"""Creates the table(s) in the database.

This module will create the database file that is set in config.py if it 
doesn't already exist.
"""
import logging
import os
import pathlib

from sqlalchemy import MetaData

import config
import models


is_db_new = not os.path.exists(config.db_filename)
logging.basicConfig(level=logging.DEBUG)

if not is_db_new:
    logging.info('The database file "%s" exists.', config.db_filename)
else:
    pathlib.Path(config.db_filename).touch()
    logging.info('The database file "%s" did not exist '
                 'and has been created.', config.db_filename)

models.Base.metadata.create_all(bind=config.engine)
metadata = MetaData(config.engine, reflect=False)
logging.info('The database "%s" has been created.', config.db_filename)
