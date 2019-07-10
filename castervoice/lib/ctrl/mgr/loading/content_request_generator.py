import glob
import os

from castervoice.lib.ctrl.mgr.loading.content_request import ContentRequest

class ContentRequestGenerator(object):
    '''
    Generates a set of requests from a list of paths.
    Later modules with the same name as earlier modules override earlier modules.
    '''
    def generate(self, content_type, *args):
        requests = {}
        for directory in args:
            # check for existence of directory
            if not os.path.isdir(directory):
                msg = "No directory '{}' was found. Could not load content from {}."
                print(msg.format(directory, directory))
                continue
            
            # get names of all python files in dir
            python_files = glob.glob(directory + "/*.py")
            module_names = [
                os.path.basename(f)[:-3]
                for f in python_files
                if not f.endswith('__init__.py')
            ]
            
            for module_name in module_names:
                requests[module_name] = ContentRequest(content_type, directory, module_name)
            
        return [requests[r] for r in requests.keys()]
    