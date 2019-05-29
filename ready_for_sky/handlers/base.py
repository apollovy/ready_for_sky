import asyncio
import os
import typing
from concurrent import futures

# noinspection PyPackageRequirements
import MySQLdb
import tornado.web
# noinspection PyPackageRequirements
from Crypto.PublicKey import RSA

DB_SERVER_HOST = os.environ['DB_SERVER_HOST']

# this will be different for every process
CONNECTION: MySQLdb.Connection = None


# noinspection PyUnusedLocal
def initializer(*args, **kwargs):
    global CONNECTION
    CONNECTION = MySQLdb.connect(
        host=DB_SERVER_HOST, passwd='example', db='ready_for_sky',
        user='root',
    )


# TODO: it's also a good idea to add a lock when the key is generated
#  to prevent IntegrityErrors and users getting 500s when simultaneously tried
#  to fetch same user's key.
# noinspection PyAbstractClass
class MainHandler(tornado.web.RequestHandler):
    executor = futures.ProcessPoolExecutor(initializer=initializer)

    async def get(self, user_name):
        key = await self.read_or_create_public_key(user_name)
        self.write(key)

    async def read_or_create_public_key(self, user_name: str):
        return await asyncio.wrap_future(
            self.executor.submit(read_or_create_public_key, user_name)
        )


# noinspection PyPep8Naming
def generate_RSA() -> typing.Tuple[bytes, bytes]:
    """
    Generate an RSA keypair with an exponent of 65537 in PEM format
    Return private key and public key

    https://gist.github.com/lkdocs/6519378
    """
    new_key = RSA.generate(4096, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")

    return private_key, public_key


def read_or_create_public_key(user_name: str) -> bytes:
    # noinspection PyTypeChecker
    maybe_key = read_public_key(CONNECTION, user_name)

    if maybe_key is None:
        # noinspection PyTypeChecker
        key = create_public_key(CONNECTION, user_name)
    else:
        key = maybe_key

    return key


def create_public_key(connection, user_name: str) -> bytes:
    cursor = connection.cursor()
    _, public_key = generate_RSA()
    sql = insert_sql()
    cursor.execute(sql, (user_name, public_key))
    connection.commit()

    return public_key


def read_public_key(connection, user_name: str) -> typing.Optional[bytes]:
    cursor = connection.cursor()
    sql = select_sql()
    cursor.execute(sql, (user_name,))
    maybe_result = cursor.fetchone()

    if maybe_result is not None:
        result = maybe_result[0].encode()
    else:
        result = maybe_result

    return result


def select_sql() -> str:
    return 'SELECT open_rsa_key FROM open_rsa_keys WHERE user_name=%s'


def insert_sql() -> str:
    return 'INSERT INTO open_rsa_keys VALUES (%s, %s)'
