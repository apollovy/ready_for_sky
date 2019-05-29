# -*- coding: utf-8 -*-


import os
# noinspection PyPackageRequirements
from Crypto.PublicKey import RSA
import tornado.web


from MySQLdb import connect


DB_SERVER_HOST = os.environ['DB_SERVER_HOST']

# noinspection PyAbstractClass
class MainHandler(tornado.web.RequestHandler):

    # @tornado.web.authenticated
    def get(self):
        self.render('index.html')


# noinspection PyPep8Naming
def generate_RSA():
    """
    Generate an RSA keypair with an exponent of 65537 in PEM format
    Return private key and public key

    https://gist.github.com/lkdocs/6519378
    """
    new_key = RSA.generate(4096, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")

    return private_key, public_key


def create_public_key(user_name: str):
    connection = connect(
        host=DB_SERVER_HOST, passwd='example', db='ready_for_sky', user='root',
    )
    assert connection.open
    cursor = connection.cursor()
    private_key, public_key = generate_RSA()
    sql = insert_sql()
    result = cursor.execute(sql, (user_name, public_key))
    connection.commit()

    return result


def select_sql():
    return 'SELECT * FROM open_rsa_keys WHERE user_name=%s'


def insert_sql():
    return 'INSERT INTO open_rsa_keys VALUES (%s, %s)'


def read_public_key(user_name: str):
    raise NotImplementedError
