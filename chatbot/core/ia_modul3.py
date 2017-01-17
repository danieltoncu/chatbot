import nltk
from nltk.tag import pos_tag
from nltk.metrics import edit_distance
from nltk.corpus import wordnet, stopwords, words
import json
import enchant
from nltk.tokenize import *
from nltk.corpus import wordnet as wn
import re
from nltk import load_parser
from nltk.stem import WordNetLemmatizer
from nltk.sem.drt import *
from nltk import wordpunct_tokenize
import string
from itertools import chain
from xml.etree.ElementTree import Element, SubElement, tostring

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


class SpellingReplacer(object):
    """
    Spell checking helper class
    """

    def __init__(self, dict_name='en_GB', max_dist=2):
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


def get_invalid_words(input_text):
    """Returns all invalid words"""
    input_words = [w for w in wordpunct_tokenize(input_text) if w.isalnum()]
    input_words_array = []

    for word in input_words:
        if wn.morphy(word) is not None:
            input_words_array.append(wn.morphy(word))
        else:
            input_words_array.append(word)

    tagged_sent = pos_tag(input_words_array)

    input_words_array = [w.lower() for w in input_words_array]

    proper_nouns = [word for word, pos in tagged_sent if pos == 'NNP']
    proper_nouns_vocab = [w.lower() for w in proper_nouns]

    cardinal_numbers = [word for word, pos in tagged_sent if pos == 'CD']

    english_vocab = set(w.lower() for w in words.words())

    invalid_words_array = []
    for word in input_words_array:
        if word not in proper_nouns_vocab and word not in cardinal_numbers:
            if word not in english_vocab:
                invalid_words_array.append(word)

    return invalid_words_array


def is_english(input_text):
    """Returns if input_text is in English"""
    input_words = [w for w in wordpunct_tokenize(input_text) if w.isalnum()]
    input_words_array = []

    for word in input_words:
        if wn.morphy(word) is not None:
            input_words_array.append(wn.morphy(word))
        else:
            input_words_array.append(word)

    tagged_sent = pos_tag(input_words_array)

    input_words_array = [w.lower() for w in input_words_array]

    proper_nouns = [word for word, pos in tagged_sent if pos == 'NNP']
    proper_nouns_vocab = [w.lower() for w in proper_nouns]

    cardinal_numbers = [word for word, pos in tagged_sent if pos == 'CD']

    english_vocab = set(w.lower() for w in words.words())
    for word in input_words_array:
        if word not in proper_nouns_vocab and word not in cardinal_numbers:
            if word not in english_vocab:
                print('Error at: ', word)
                return False
    return True


def detect_english_similarity_proportion(input_text):
    input_words = set([w for w in wordpunct_tokenize(input_text) if w.isalnum()])
    invalid_proportion = 100 * (len(input_words) - len(get_invalid_words(input_text))) / len(input_words)
    return invalid_proportion


def get_language_likelihood(text):
    """
    Returns a dictionary of languages and their likelihood of being the
    natural language of the input text
    """
    text = text.lower()
    input_words = wordpunct_tokenize(text)

    language_likelihood = {}
    for language in stopwords._fileids:
        language_likelihood[language] = len(set(input_words) &
                                            set(stopwords.words(language)))

    return language_likelihood


def get_language(text):
    """
    Returns the most likely language of the given text
    """
    likelihoods = get_language_likelihood(text)
    return sorted(likelihoods, key=likelihoods.get, reverse=True)[0]


def get_sentences(text):
    """
    Function used to get the sentences from a text.
    """
    text = spell_check(text)
    sentences = tokenizer.tokenize(text)
    return sentences


def get_tagged(text):
    text = spell_check(text)
    sentences = get_sentences(text)
    tagged = []
    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        tagged += nltk.pos_tag(tokens)
    return tagged


def get_entities(text):
    text = spell_check(text)
    sentences = get_sentences(text)
    tagged = get_tagged(text)
    entities = nltk.chunk.ne_chunk(tagged)
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
                  json_append_mode=False,
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


def find_anaphora(input_text):
    parser = load_parser(os.path.join("chatbot", "core", "drt.fcfg"), logic_parser=DrtParser())
    sentences = sent_tokenize(input_text)
    list_anaphora = []
    drs_list = []
    for sentence in sentences:
        lst_words = word_tokenize(sentence)
        words_number = len(lst_words)
        words_without_punctuations = []
        for i in range(words_number - 1):
            if lst_words[i] not in string.punctuation:
                words_without_punctuations.append(lst_words[i])
        list_anaphora.append(words_without_punctuations)
    for i in range(len(list_anaphora)):
        try:
            trees = list(parser.parse(list_anaphora[i]))
        except Exception:
            return None, None
        if len(trees) > 0:
            drs_list.append(trees[0].label()['SEM'].simplify())
    expressions = ""
    drt_expression = DrtExpression.fromstring
    for drs in drs_list:
        drs_expr = drt_expression(str(drs))
        expressions += str(drs_expr) + " + "
    expressions = expressions[:-3]
    expressions = drt_expression(expressions)
    anaphora = str(expressions.simplify().resolve_anaphora())
    actual_index = anaphora.find('],[')
    expression_anaphora = anaphora[actual_index + 3:-2]
    print("8",expression_anaphora)
    return expression_anaphora, sentences


def format_output(sentence, extracted_sentences):
    words_sentence = []
    lemmatizer = WordNetLemmatizer()
    words_lst = pos_tag(word_tokenize(sentence))
    words_lst[1] = [w[1].lower() for w in words_lst
                    if w[1] is not string.punctuation and words_lst[1] not in ['NNPS', 'NNP']]
    for word in words_lst:
        if word[1] in string.punctuation:
            continue
        word_base_form = lemmatizer.lemmatize(word=word[0])
        synonyms = get_synonyms(word_base_form)
        if words_lst[1] in ['NNPS', 'NNP']:
            continue
        words_sentence.append(sentence)
        if len(extracted_sentences) > 0 and extracted_sentences[0][0] == word[0]:
            words_sentence.append("find_this:" + extracted_sentences[0][0])
            if extracted_sentences[0][2] is not None:
                words_sentence.append("anaphora:" + extracted_sentences[0][2])
        for i in range(len(synonyms) - 1):
            words_sentence.append("synonym:" + synonyms[i])
    return words_sentence


def resolve_anaphora(input_text):
    expression_anaphora, sentences = find_anaphora(input_text)
    if expression_anaphora is None:
        print("Couldn't resolve anaphora , some words are not in the grammar")
        return None
    pattern = "\(*(\w+)\((\w+)\)*( = \(\w+ = (\[\w+(,\w+)*\])\))?\)*"
    variables = expression_anaphora.split(', ')
    print(variables[0])
    extracted_words = list(
        chain.from_iterable(((re.match(pattern, variable)).group(1), (re.match(pattern, variable)).group(2),
                             (re.match(pattern, variable)).group(4)) for variable in variables
                            if re.match(pattern, variable) is not None))
    tree2 = [list((extracted_words[i], extracted_words[i + 1], extracted_words[i + 2]))
             for i in range(0, len(extracted_words), 3)]
    return_list = []
    for sentence in sentences:
        return_list.append(format_output(sentence, tree2))

    for lst in return_list:
        print(lst)
    return return_list

# print(detect_english_similarity_proportion(
#     "A small sample osf texts from Project Gutenberg appears in the NLTK collection. 101cm 2 4th"), "%")
# print(get_language("A small sample osf texts from Project Gutenberg appears in the NLTK collection. 101cm 2 4th"))
# print(get_language_likelihood(
#     "A small sample of texts from Project Gutenberg appears in the NLTK collection. 101cm 2 4th"))
# print(get_invalid_words("A small sample osf texts from Project Gutenberg appears in the NLTK collection. 101cm 2 4th"))
# print(is_english("A small sample of texts from Project Gutenberg appears in the NLTK collection. 101cm 2 4th"))

# text = "Anna has two eyes. Dan doesn't like Ben."
# generate_json(text, "data.txt")
# print(WordNetLemmatizer().lemmatize("She has apples"))
# print(resolve_anaphora("Joe owns a dog. He owns Joe."))
