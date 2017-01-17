"""Chatbot application main."""

import sys

import cherrypy

from backend.web_server import ChatbotWebServer
import config

from core.chatbot import Chatbot


def main(multiple_answers):

	chatbot = Chatbot("Jarvis", multiple_answers)

	cherrypy.quickstart(ChatbotWebServer(config.WEB_PAGES_BASEDIR, chatbot), '/', config.conf)


if __name__ == "__main__":

	multiple_answers = False

	if len(sys.argv) > 2:
		print("\n Usage: %s [--multiple-answers]\n" % sys.argv[0])
		sys.exit()
	elif (len(sys.argv) == 2) and (sys.argv[1] == "--multiple-answers"):
		multiple_answers = True

	# execute only if run as a script
	main(multiple_answers)
