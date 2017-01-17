import wikipedia

def wikipedia_search(search_word):
    try:
        response = "I found this on Wikipedia:\n" + wikipedia.summary(search_word, sentences=1)
        return response
    except wikipedia.exceptions.DisambiguationError as e:
        print "Too ambiguous for Wikipedia"
    return ""

# print wikipedia_search("Barrack Obama")