import os

# noinspection PyPackageRequirements
import pytest
# noinspection PyPackageRequirements
from MySQLdb import connect

from handlers import base

PRIVATE_KEY = b'''i'm so private'''
PUBLIC_KEY = b'''i'm so public'''


# noinspection PyPep8Naming
def _generate_RSA():
    return PRIVATE_KEY, PUBLIC_KEY


@pytest.fixture
def generate_rsa_patched(monkeypatch):
    monkeypatch.setattr(base, 'generate_RSA', _generate_RSA)


@pytest.fixture
def db_server_host():
    return os.environ['DB_SERVER_HOST']


@pytest.fixture
def mysql_connection(db_server_host):
    connection = connect(
        host=db_server_host, passwd='example', db='ready_for_sky', user='root',
    )

    return connection


@pytest.fixture
def table_cleared(mysql_connection):
    mysql_connection.cursor().execute('DELETE FROM open_rsa_keys WHERE true')
    mysql_connection.commit()


@pytest.fixture
def user_name():
    return 'barsuk'


@pytest.fixture
def public_key_created(mysql_connection, user_name):
    result = base.create_public_key(mysql_connection, user_name)

    return result


@pytest.fixture
def public_key_read(mysql_connection, user_name):
    result = base.read_public_key(mysql_connection, user_name)

    return result


@pytest.fixture
def public_key_read_or_created(mysql_connection, user_name):
    key = base.read_or_create_public_key(mysql_connection, user_name)

    return key


def test_mysql_connection_works(mysql_connection):
    assert mysql_connection.open


def test_public_key_creates_successfully(table_cleared, public_key_created):
    assert public_key_created


def test_public_key_reads(
        table_cleared, generate_rsa_patched,
        mysql_connection, public_key_created, public_key_read,
):
    assert public_key_read == PUBLIC_KEY


def test_public_key_reads_or_creates(
        table_cleared, generate_rsa_patched,
        mysql_connection, public_key_read_or_created,
):
    assert public_key_read_or_created == PUBLIC_KEY


def test_generated_keys_are_bytes():
    private, public = base.generate_RSA()
    assert isinstance(private, bytes)
    assert isinstance(public, bytes)
