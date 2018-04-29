import time
def err():
    raise Exception("Invalid level!", "error")
while True:
    try:
        err()
    except Exception,e:
        print e
        time.sleep(3)