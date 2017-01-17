"""Chatbot module."""

from ia_modul3 import spell_check
from ia_modul3 import get_entities
from aiml_parser import aiml_response
from wikipedia_search import wikipedia_search
from google_search import google_search


class Chatbot(object):

    def __init__(self, name, multiple_answers=False):
        self.name = name
        self._multiple_answers = multiple_answers

    def get_answer(self, question):

        # We try to find an answer in all of our services
        possible_answers = {}

        corrected_question = spell_check(question)

        entities = get_entities(corrected_question)

        # First, we try to find an answer in our local AIML files
        possible_answers["AIML"] = aiml_response(corrected_question)

        if not self._multiple_answers and possible_answers["AIML"] != "":
            return possible_answers["AIML"]

        # We search on Wikipedia only if the question starts with `WHO` or `WHAT`;
        # but if it is too ambiguous, we still perform a Google Search.

        if "WP" in entities.values():
            search_words = ""
            for k, v in entities.iteritems():
                if v == "NNP":
                    search_words += k + " "

            possible_answers["Wikipedia"] = wikipedia_search(search_words[:-1])

            if possible_answers["Wikipedia"] == "":
                possible_answers["Google"] = google_search(corrected_question)

            if not self._multiple_answers and possible_answers["Wikipedia"] != "":
                return possible_answers["Wikipedia"]

            if not self._multiple_answers and possible_answers["Google"] != "":
                return possible_answers["Google"]

        # We search on Google only if the question starts with `WHERE`, `WHEN`, `WHOSE`, `WHICH`.
        if any(pronoun in entities.values() for pronoun in ["WDT", "WP$", "WRB"]):
            possible_answers["Google"] = google_search(corrected_question)

            if not self._multiple_answers and possible_answers["Google"] != "":
                return possible_answers["Google"]

        if not self._multiple_answers:
            return "What? I even don't know how to answer. Maybe you tell me!?"
        else:
            answer = ""
            for k, v in possible_answers.iteritems():
                if v != "":
                    answer += v + " ({})\n".format(k)
            answer = answer[:-1]

            if answer == "":
                answer = "What? I even don't know how to answer. Maybe you tell me!?"

            return answer
