import googleAPI
from time import time
from threading import Thread

def addTree(url, strings, index):
    tree = handle.getTree(link)
    if tree is not None:
        strings[index] = tree.xpath("//p/text()")
    else:
        strings[index] = []


while True:
    handle = googleAPI.googleAPI()
    threads = []

    inputString = input("Type search query >")

    times = [time(), time()]
    targets = handle.getGoogleURLs(inputString)
    strings = [[] for x in targets]

    for linkIndex in range(len(targets)):
        link = targets[linkIndex]

        process = Thread(target=addTree, args=[link, strings, linkIndex])
        process.start()
        threads.append(process)

    for process in threads:
        process.join()

    cleanStrings = [strings[x] for x in range(len(strings)) if not len(strings[x]) == 0]
    del strings

# split the paragraphs into an array
#    for i in range(0, len(string)):
#        for ii in range(0, len(string[i])):
#            string[i][ii] = string[i][ii]
#            splits.append(string[i][ii].encode('ascii', 'ignore').split())
    times[1] = time()
#    for i in string:
    c = sum(map(len, cleanStrings))

    print("Search executed in {} seconds with {} paragraphs found.".format((times[1]-times[0]), c))
    pass
    del threads, targets, cleanStrings

