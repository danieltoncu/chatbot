"""Chatbot application main."""

import cherrypy

from backend.web_server import ChatbotWebServer
import config

from core.chatbot import Chatbot


def main():

	chatbot = Chatbot("Jarvis")

	cherrypy.quickstart(ChatbotWebServer(config.WEB_PAGES_BASEDIR, chatbot), '/', config.conf)


if __name__ == "__main__":
	# execute only if run as a script
	main()
