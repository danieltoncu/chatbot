"""CherryPy Server for ChatBot application."""

import os, os.path

import cherrypy


class ChatbotWebServer(object):

	def __init__(self, web_pages_basedir, chatbot):
		self._web_pages_basedir = web_pages_basedir
		self._chatbot = chatbot

	@cherrypy.expose
	def index(self):
		return open(os.path.join(self._web_pages_basedir, "index.html"))

	@cherrypy.expose
	def get_answer(self, question):
		return self._chatbot.get_answer(question)
