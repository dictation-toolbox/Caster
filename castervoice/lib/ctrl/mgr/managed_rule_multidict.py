from castervoice.lib import printer

'''TODO: delete this, didn't end up using it'''
class ManagedRuleMultiDict(object):
    """
    Keeps references to managed rules via multiple keys.
    Does not throw exceptions when a key is not found in dict.
    Presently only uses pronunciation
    """

    def __init__(self):
        self._names = {}
        self._executables = {}
        self._grammar_names = {}
        self._pronunciations = {}
        self._class_names = {}
        self._file_paths = {}

    def put(self, managed_rule):
        instance = managed_rule.get_rule_instance()
        file_path = self._get_file_path(managed_rule, instance)

        if managed_rule.details.name is not None:
            self._names[managed_rule.details.name] = managed_rule
        if managed_rule.details.executable is not None:
            self._executables[managed_rule.details.executable] = managed_rule
        if managed_rule.details.grammar_name is not None:
            self._grammar_names[managed_rule.details.grammar_name] = managed_rule
        if managed_rule.details.ccrtype is not None:
            self._pronunciations[instance.get_pronunciation()] = managed_rule
        self._file_paths[file_path] = managed_rule
        self._class_names[managed_rule.get_rule_class_name()] = managed_rule

    def get_by_name(self, name):
        return None if name not in self._names else self._names[name]

    def get_by_executable(self, executable):
        return None if executable not in self._executables else self._executables[executable]

    def get_by_grammar_name(self, grammar_name):
        return None if grammar_name not in self._grammar_names else self._grammar_names[grammar_name]

    def get_by_pronunciation(self, pronunciation):
        return None if pronunciation not in self._pronunciations else self._pronunciations[pronunciation]

    def get_by_class_name(self, class_name):
        return None if class_name not in self._class_names else self._class_names[class_name]

    def get_by_file_path(self, file_path):
        return None if file_path not in self._file_paths else self._file_paths[file_path]

    '''TODO: warn about rule signature changes -- when the set of keys is updated in a file change'''

    def _check_for_signature_change(self, managed_rule, instance):
        """
        A "signature change" is when, during file editing, someone changes a rule's "details"
        object. This might work out fine, or might cause unexpected behavior, depending on the
        type of change. Signature changes will print warnings, but not cause rejections.

        THIS METHOD IS ONLY RELIABLE when key information is added, not when it is removed.
        It also may not be reliable for class name or file name changes. It's a best-guess
        warning system ONLY.

        :param managed_rule: a ManagedRule
        :return:
        """

        pronunciation = self._get_pronunciation(managed_rule, instance)
        class_name = managed_rule.get_rule_class_name()
        file_path = self._get_file_path(managed_rule, instance)

        # see rule is already available under any of its keys
        by_name = self.get_by_name(managed_rule.details.name)
        by_executable = self.get_by_executable(managed_rule.details.executable)
        by_grammar_name = self.get_by_grammar_name(managed_rule.details.grammar_name)
        by_pronunciation = self.get_by_pronunciation(pronunciation)
        by_class_name = self.get_by_class_name(class_name)
        by_file_path = self.get_by_file_path(file_path)

        changes = []

        # first look for added information
        changes.extend(self._check_for_added_info(managed_rule.details.name, by_name, "name"))
        changes.extend(self._check_for_added_info(managed_rule.details.executable, by_executable, "executable"))
        changes.extend(self._check_for_added_info(managed_rule.details.grammar_name, by_grammar_name, "grammar_name"))
        changes.extend(self._check_for_added_info(pronunciation, by_pronunciation, "pronunciation"))
        changes.extend(self._check_for_added_info(class_name, by_class_name, "class_name"))
        changes.extend(self._check_for_added_info(file_path, by_file_path, "file_path"))

        # then look for changed/removed information
        found_it = by_name is not None or by_executable is not None \
                   or by_grammar_name is not None or by_pronunciation is not None \
                   or by_class_name is not None or by_file_path is not None
        changes.extend(self._check_for_changed_or_removed_info(found_it, by_name, "name"))
        changes.extend(self._check_for_changed_or_removed_info(found_it, by_executable, "executable"))
        changes.extend(self._check_for_changed_or_removed_info(found_it, by_grammar_name, "grammar_name"))
        changes.extend(self._check_for_changed_or_removed_info(found_it, by_pronunciation, "pronunciation"))
        changes.extend(self._check_for_changed_or_removed_info(found_it, by_class_name, "class_name"))
        changes.extend(self._check_for_changed_or_removed_info(found_it, by_file_path, "file_path"))

        # filter out null results
        changes = [change for change in changes if change is not None]
        if len(changes) > 0:
            printer.out("WARNING: changes to details detected for " + class_name + ": " + ", ".join(changes))

    def _check_for_added_info(self, key, search_result, property_name):
        added = key is not None and search_result is None
        return "'" + property_name + "' was added" if added else None

    def _check_for_changed_or_removed_info(self, exists, search_result, property_name):
        exists_but_not_found = exists and search_result is None
        return "'" + property_name + "' was changed or removed" if exists_but_not_found else None

    def _get_file_path(self, managed_rule, instance):
        if managed_rule.details.declared_ccrtype is not None:
            return instance.location
        else:
            return managed_rule.details.file_path

    def _get_pronunciation(self, managed_rule, instance):
        return None if managed_rule.declared_ccrtype is None else instance.get_pronunciation()