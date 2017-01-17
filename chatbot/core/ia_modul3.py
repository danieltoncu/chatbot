import nltk
from nltk import wordpunct_tokenize
from nltk.tag import pos_tag
from nltk.metrics import edit_distance
from nltk.corpus import wordnet, stopwords, words
import json
import enchant

from enchant.checker import SpellChecker

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

'''
Spell checking helper class
'''
class SpellingReplacer(object):
    def __init__(self, dict_name = 'en_GB', max_dist = 2):
        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = 2

    def replace(self, word):
        if self.spell_dict.check(word):
            return word
        suggestions = self.spell_dict.suggest(word)

        if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
            return suggestions[0]
        else:
            return word

'''
Function used to spell check text.
'''
def spell_check(text):
    word_list = text.split()
    checked_list = []
    for item in word_list:
        replacer = SpellingReplacer()
        r = replacer.replace(item)
        checked_list.append(r)
    return ' '.join(checked_list)

######

'''
Language detection utils
'''

'''
    Returns a dictionary of languages and their likelihood of being the
    natural language of the input text
'''
def get_language_likelihood(text):
    
    text = text.lower()
    input_words = wordpunct_tokenize(text)

    language_likelihood = {}
    total_matches = 0
    for language in stopwords._fileids:
        language_likelihood[language] = len(set(input_words) &
                                            set(stopwords.words(language)))

    return language_likelihood

'''
    Returns the most likely language of the given text
'''
def get_language(text):
    
    likelihoods = get_language_likelihood(text)
    return sorted(likelihoods, key=likelihoods.get, reverse=True)[0]

'''
Returns all invalid words
'''
def get_invaid_words(text):
    text_vocab = set(w.lower() for w in wordpunct_tokenize(text))
    english_vocab = set(w.lower() for w in words.words())
    unusual = text_vocab - english_vocab
    return sorted(unusual)

'''
Returns if input_text is in English
'''
def is_english(text):
    input_words = wordpunct_tokenize(text)
    tagged_sent = pos_tag(text.split())

    propernouns = [word for word, pos in tagged_sent if pos == 'NNP']

    for word in input_words:
        if not word in propernouns:
            if not word in words.words():
                return False
    return True


########
'''
Function used to get the sentences from a text.
'''
def get_sentences(text):
    text = spell_check(text)
    sentences = tokenizer.tokenize(text)
    return sentences


def get_tagged(text):
    text = spell_check(text)
    sentences = get_sentences(text)
    tagged = []
    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        tagged +=  nltk.pos_tag(tokens)
    return tagged

def get_entities(text):
    text = spell_check(text)
    sentences = get_sentences(text)
    tagged_entities = get_tagged(text)
    # entities = nltk.chunk.ne_chunk(tagged_entities)
    entities = {}
    for entity in tagged_entities:
        entities[entity[0]] = entity[1]
    return entities

def get_synonyms(text):
    text = spell_check(text)
    s = {}
    tokens = nltk.word_tokenize(text)
    for word in tokens:
        synonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                if l.name() != word and l.name() not in synonyms:
                    synonyms.append(l.name())
        if len(synonyms) > 0:
            s[word] = synonyms
    return s

def get_antonyms(text):
    text = spell_check(text)
    a = {}
    tokens = nltk.word_tokenize(text)
    for word in tokens:
        antonyms = []
        for ant in wordnet.synsets(word):
            for l in ant.lemmas():
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())
        if len(antonyms) > 0:
            a[word] = antonyms
    return a


def generate_json(text, 
    json_path, 
    json_append_mode = False,
    sentences=True, 
    tagged=True, 
    entities=True,
    synonyms=True,
    antonyms=True):

    if json_append_mode is True:
        mode = 'a'
    else:
        mode = 'w'

    whole = {}

    if sentences is True:
        whole["sentences"] = get_sentences(text)
    if tagged is True:
        whole["tagged"] = get_tagged(text)
    if entities is True:
        whole["entities"] = get_entities(text)
    if synonyms is True:
        whole["synonyms"] = get_synonyms(text)
    if antonyms is True:
        whole["antonyms"] = get_antonyms(text)

    with open(json_path, mode) as outfile:
        json.dump(whole, outfile, indent=4)


text = "Where is Paris?"
# print spell_check(text)
entities = get_entities(text)
# print entities
generate_json(text, "processed_sentence.txt")

