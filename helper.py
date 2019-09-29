import random
import time

def check_follow_limit(followed, limit):
    if followed >= limit:
        return True
    return False


def wait_random_time(waitLong):
    if waitLong:
        i = random.randint(20,60)
        print("Waiting for {} seconds".format(i))
        time.sleep(i)
    else:
        i = random.randint(3,6)
        print("Waiting for {} seconds".format(i))
        time.sleep(i)
