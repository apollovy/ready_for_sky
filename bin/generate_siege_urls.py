import random
import string


def generate_random_word(size):
    return ''.join(random.sample(
        string.digits + string.ascii_letters, size,
    ))


if __name__ == '__main__':
    for _ in range(100):
        print('http://localhost:8000/' + generate_random_word(4))
