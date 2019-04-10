
from inspect           import getargspec
from dragonfly.actions.action_base import ActionBase, ActionError

# tweaked version of function action for dealing with the case when the argument names
# from the extras don't match the argument names in the function signature
# be careful of name conflict. the default arguments must not be named remap_data!


class RemapArgsFunction(ActionBase):
    def __init__(self, function, remap_data=None, **defaults):
    # alternative that would avoid name conflict:  def __init__(self, function, defaults=None, remap_data=None):
    
        ActionBase.__init__(self)
        self._function = function
        self._defaults = defaults or {}
        self._remap_data = remap_data or {}
        self._str = function.__name__

        # TODO Use inspect.signature instead; getargspec is deprecated.
        (args, varargs, varkw, defaults) = getargspec(self._function)
        if varkw:  self._filter_keywords = False
        else:      self._filter_keywords = True
        self._valid_keywords = set(args)

    def _execute(self, data=None):
        arguments = dict(self._defaults)
        if isinstance(data, dict):
            arguments.update(data)

        # Remap specified names.
        if arguments and self._remap_data:
            for old_name, new_name in self._remap_data.items():
                if old_name in data:
                    arguments[new_name] = arguments.pop(old_name)

        if self._filter_keywords:
            invalid_keywords = set(arguments.keys()) - self._valid_keywords
            for key in invalid_keywords:
                del arguments[key]

        try:
            self._function(**arguments)
        except Exception as e:
            self._log.exception("Exception from function %s:"
                                % self._function.__name__)
            raise ActionError("%s: %s" % (self, e))
