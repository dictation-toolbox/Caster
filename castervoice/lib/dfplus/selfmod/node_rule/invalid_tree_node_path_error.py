class InvalidTreeNodePathError(Exception):
    def __init__(self, active_path):
        super("Broken TreeNode path: {}".format(str(active_path)))