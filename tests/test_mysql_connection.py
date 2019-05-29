from MySQLdb import connect


def test_mysql_connection_works():
    connection = connect(host='db', passwd='example')
    assert connection.open
