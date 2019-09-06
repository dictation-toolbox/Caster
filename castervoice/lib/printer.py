def out(message, *args):
    """
    Use this as a printing interface to send messages to places other than the console.
    DO NOT import anything in this class. Use *args.
    """
    if len(args) > 0:
        print([message] + list(args))
    else:
        print(message)
