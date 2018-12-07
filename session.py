"""Module to manage database sessions"""
from contextlib import contextmanager


@contextmanager
def session_scope(session):
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
