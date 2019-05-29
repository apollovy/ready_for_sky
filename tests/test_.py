import os

# noinspection PyPackageRequirements
import pytest
# noinspection PyPackageRequirements
from MySQLdb import connect

from handlers.base import create_public_key


@pytest.fixture
def db_server_host():
    return os.environ['DB_SERVER_HOST']


def test_mysql_connection_works(db_server_host):
    connection = connect(
        host=db_server_host, passwd='example', db='ready_for_sky', user='root',
    )
    assert connection.open


def test_public_key_creates_successfully():
    result = create_public_key('barsuk')
    assert result
