import googleAPI
import pronouncing
from random import randint
from time import time
from threading import Thread

def addTree(url, strings, index):
    tree = handle.getTree(link)
    if tree is not None:
        strings[index] = tree.xpath("//p/text()")
    else:
        strings[index] = []

def addCandidates(strings, index):
    lastWord = ''.join(filter(str.isalnum, strings[index]["string"].strip().split(" ")[-1])).lower()
    strings[index]["candidates"] = pronouncing.rhymesFast(lastWord)
    strings[index]["lastWord"] = lastWord

def canRhyme(s):
    if "candidates" in s:
        return len(s["candidates"]) > 0
    else:
        return False

def hasMatch(s):
    return len(s["matches"]) > 0


def helpSort(s):
    return s["syllables"]


pronouncing.init_cmu()
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
            # Remove unwanted characters from strings
            for c in ["\\", "]", "[", "/", "\"", "'"]: strings[x] = strings[x].replace(c, "")
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

    # Find all rhyme candidates for each string
    for x in range(len(strings)):
        addCandidates(strings, x)

    times[1] = time()



    # Wait for threads to finish processing
    #for process in threads:
    #    process.join()

    times[1] = time()
    c = len(strings)
    print("It took {} seconds to process {} words at a rate of {} words per second".format(times[1] - times[0], c, c /
                                                                                    (times[1] + 0.00001 - times[0])))

    # Remove strings that have no rhyme candidates
    strings = list(filter(canRhyme, strings))
    print("Removed {} entries // {}% of total".format(c-len(strings), int((c-len(strings)) / c * 100)))

    times = [time(), time()]

    # Add syllable count to strings
    for x in range(len(strings)): strings[x]["syllables"] = pronouncing.syllable_count_string(strings[x]["string"])

    # Sort strings by number of syllables
    strings = sorted(strings, key=helpSort)[::-1]

    # Prepare strings for rhyme matches
    for x in range(len(strings)): strings[x]["matches"] = []


    # Link sentences that rhyme
    # TODO: Improve this algorithm by .extend()ing matches
    for x in range(len(strings)):
        for xx in range(x + 1, len(strings)):
            if(strings[xx]["lastWord"] in strings[x]["candidates"]):
                #strings[x]["matches"].extend(strings[xx]["matches"])
                #strings[xx]["matches"].extend(strings[x]["matches"])
                strings[x]["matches"].append(xx)
                strings[xx]["matches"].append(x)
                #print("{}  //  {}".format(len(strings[x]["matches"]), len(strings[xx]["matches"])))

    #strings = list(filter(hasMatch, strings))

    times[1] = time()
    cc = sum(map(len, (strings[x]["matches"] for x in range(len(strings))))) // 2
    print("It took {} seconds to find approximately {} rhyming sentences from {} total sentences".format(
        times[1] - times[0], cc, c))



    for i in range(len(strings)):
        dummy = input("Press Enter\n")
        print(strings[i]["string"], " // ", len(strings[i]["matches"]))
        for match in strings[i]["matches"]:
            print(strings[match]["string"])

    del threads, targets, strings

