'''
Hooks are merge-time events which, unlike transformers,
do NOT mutate mergerules. They may be run at various 
points throughout the merge process.
'''
class BaseHook(object):
    def run(self, event):
        pass