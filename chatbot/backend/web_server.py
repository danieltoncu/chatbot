"""CherryPy Server for ChatBot application."""

import cherrypy


class ChatbotWebServer(object):

	def __init__(self):
		self._chatbot = None

	@cherrypy.expose
	def index(self):
		return open("frontend/index.html")

	@cherrypy.expose
	def get_answer(self, question):
		return "Unimplemented."
