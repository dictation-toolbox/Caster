from dragonfly import RecognitionHistory


def get_and_register_history(utterances=10):
    history = RecognitionHistory(utterances)
    history.register()
    return history
