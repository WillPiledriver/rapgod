import googleAPI
import pronouncing
from time import time, sleep
from threading import Thread, activeCount

def addTree(url, strings, index):
    tree = handle.getTree(link)
    if tree is not None:
        strings[index] = tree.xpath("//p/text()")
    else:
        strings[index] = []

def addCandidates(strings, index):
    strings[index]["candidates"] = pronouncing.rhymes(strings[index]["string"].split(" ")[-1].replace(".", ""))


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

    threads = []

    # Trim all whitespace and remove any strings with less than 3 words
    strings = [[strings[x][xx].strip()  for xx in range(len(strings[x])) if strings[x][xx].strip().count(" ") > 1] for x in range(len(strings)) if len(strings[x]) > 0]

   # Remove any blank elements
    strings = [strings[x] for x in range(len(strings)) if len(strings[x]) > 0]

    # Convert variable to one-dimensional array, and remove any duplicate paragraphs
    strings = list(set([strings[x][xx] for x in range(len(strings)) for xx in range(len(strings[x]))]))

    # Break paragraphs down into sentences or independent clauses*
    #                                                              *results will vary
    for delimiter in [". ", "! ", "? ", "\n", "\t", "\r"]:
        for x in range(len(strings)):
            # Removing unwanted characters from strings
            for c in ["\\", "]", "[", "/"]: strings[x] = strings[x].replace(c, "")
            paragraph = strings[x].split(delimiter)
            if len(paragraph) > 1:
                strings[x] = paragraph[0]
                for xx in range(1, len(paragraph)):
                    strings.append(paragraph[xx])

    # Finally, removes any blank strings and sentences with under 3 words
    strings = [strings[x] for x in range(len(strings)) if strings[x] is not "" and strings[x].count(" ") > 1]

    times[1] = time()
    print("Search executed in {} seconds with {} paragraphs found.".format((times[1]-times[0]), len(strings)))
    times = [time(), time()]

    # Prepare strings variable to receive rhyme candidates
    strings = [{"string": strings[x]} for x in range(len(strings))]

    # Start a new thread for each string to find out all the rhyme candidates
    # Maximum thread pool for this process is 50 threads.
    x = 0
    while x < len(strings):
        if activeCount() < 50:
            process = Thread(target=addCandidates, args=[strings, x])
            process.start()
            threads.append(process)
            if x % 100 == 0:
                print(str(int(x / len(strings) * 100)) + "% complete")
            if x == len(strings):
                break
            x += 1
        sleep(0.025)

    # Wait for threads to finish processing
    for process in threads:
        process.join()

    times[1] = time()
    print("It took {} seconds to finish finding all the rhyme candidates".format(times[1]-times[0]))


    # TODO: Remove strings that have no rhyme candidates
    # TODO: Match rhyming sentences

    del threads, targets, strings

