"""Chatbot module."""


class Chatbot(object):

	def __init__(self, name):
		self.name = name

	def get_answer(self, question):
		return "This should be an answer to the question \"{}\".".format(question)
