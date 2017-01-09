"""CherryPy Server for ChatBot application."""

import cherrypy


class ChatbotWebServer(object):

	def __init__(self, chatbot):
		self._chatbot = chatbot

	@cherrypy.expose
	def index(self):
		return open("frontend/index.html")

	@cherrypy.expose
	def get_answer(self, question):
		return self._chatbot.get_answer(question)
