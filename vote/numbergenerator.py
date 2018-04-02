import random
import string

#class booth:
 #   def __init__(self):


def getkey(booth):
    #boothkeys = [x.key for x in booth]
    #boothkeys = []
    boothkeys = booth
    key = None

    while True:
        key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=6))
        if not key in boothkeys:
            break


    return key

if __name__ == "__main__":

    list = ['rFKeel','tOLpZV','pldygS']

    print(getkey(list))


    #example = ''.join(random.choices(string.ascii_uppercase+string.ascii_lowercase, k=6))
    #print(example)




