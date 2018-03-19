def readnumbers(filename):
    numbers = []
    file = open(filename,"r")

    for line in file:
        line = line.split()
        numbers.append(str(line))

    file.close()
    return numbers


def confirm(filetocheck,numtocheck):
    fromfile = readnumbers(filetocheck)

    checker = True

    temp = "['"+numtocheck+"']"
    #print (temp)

    if temp in fromfile:
        checker = True
    else:
        checker = False
    return checker

if __name__ == "__main__":
    print(confirm("example.txt","FBAOAO"))

    #wtf = readnumbers("example.txt")

    #print (wtf)
    #print(isinstance(wtf[1], str))


