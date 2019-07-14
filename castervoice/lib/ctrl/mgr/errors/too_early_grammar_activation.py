class TooEarlyGrammarActivatorError(Exception):
    def __init__(self):
        super("Do not attempt to build the activation rule before setting the de/activator functions.")