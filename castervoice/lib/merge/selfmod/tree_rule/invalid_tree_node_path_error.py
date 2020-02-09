class InvalidTreeNodePathError(Exception):
    def __init__(self, active_path):
        super(InvalidTreeNodePathError, self).__init__("Broken TreeNode path: {}".format(str(active_path)))