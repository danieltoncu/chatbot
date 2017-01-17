import aiml
import os

kernel = aiml.Kernel()
aiml_dir = os.path.join("chatbot", "core", "aiml-dir")
brain = os.path.join(aiml_dir, 'bot_brain.brn')

if os.path.isfile(brain):
    kernel.bootstrap(brainFile= brain)
else:
    files = os.listdir(aiml_dir)
    for file in files:
        kernel.learn(aiml_dir + '/' + file)
    kernel.saveBrain(brain)

def aiml_response(message):
    bot_response = kernel.respond(message)
    return bot_response
