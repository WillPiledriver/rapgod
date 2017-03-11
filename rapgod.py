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

    # Get search query and collect urls from google

    times = [time(), time()]
    targets = handle.getGoogleURLs(inputString)
    strings = [[] for x in targets]

    # Start a new thread for each target webpage collection to speed process
    for linkIndex in range(len(targets)):
        link = targets[linkIndex]

        process = Thread(target=addTree, args=[link, strings, linkIndex])
        process.start()
        threads.append(process)

    # Wait for threads to finish processing
    for process in threads:
        process.join()

    # Trim all whitespace and remove blank elements from the strings
    strings = [[strings[x][xx].strip() for xx in range(len(strings[x])) if strings[x][xx].strip().count(" ") > 1] for x in range(len(strings)) if len(strings[x]) > 0]
    strings = [strings[x] for x in range(len(strings)) if len(strings[x]) > 0]


    times[1] = time()
    c = sum(map(len, strings))

    print("Search executed in {} seconds with {} paragraphs found.".format((times[1]-times[0]), c))
    times = [time(), time()]

    # TODO: Find most efficient way to build a matrix of rhyming strings


    del threads, targets, strings

