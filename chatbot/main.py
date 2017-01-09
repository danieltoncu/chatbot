"""Chatbot application main."""

import cherrypy

from backend.web_server import ChatbotWebServer
import config


def main():

	cherrypy.quickstart(ChatbotWebServer(), '/', config.conf)


if __name__ == "__main__":
	# execute only if run as a script
	main()
