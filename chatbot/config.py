"""Configuration settings for CherryPy Server."""

import os, os.path


conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'frontend'
    }
}

WEB_PAGES_BASEDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
