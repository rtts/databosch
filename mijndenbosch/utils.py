import os, random, string

CHARS = string.ascii_letters+string.digits

def random_string(length):
    """Returns a random alphanumeric string"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(length))
