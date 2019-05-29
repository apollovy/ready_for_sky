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


def create_public_key(connection, user_name: str):
    cursor = connection.cursor()
    _, public_key = generate_RSA()
    sql = insert_sql()
    result = cursor.execute(sql, (user_name, public_key))
    connection.commit()

    return result


def read_public_key(connection, user_name: str):
    cursor = connection.cursor()
    sql = select_sql()
    cursor.execute(sql, (user_name, ))
    result = cursor.fetchone()

    return result


def select_sql():
    return 'SELECT open_rsa_key FROM open_rsa_keys WHERE user_name=%s'


def insert_sql():
    return 'INSERT INTO open_rsa_keys VALUES (%s, %s)'
