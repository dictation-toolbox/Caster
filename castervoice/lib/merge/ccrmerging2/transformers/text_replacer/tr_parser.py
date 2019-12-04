import io
import os

from castervoice.lib import settings
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.tr_definitions import TRDefinitions
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.tr_parse_mode import TRParseMode


class TRParser(object):
    """
    Reads text replacement definitions from words.txt.
    """

    def create_definitions(self):
        lines = self._get_lines()
        return self._parse_lines(lines)

    def _get_lines(self):
        words_txt_path = settings.settings(["paths", "GDEF_FILE"])
        words_txt_lines = []
        if os.path.isfile(words_txt_path):
            with io.open(words_txt_path, "rt", encoding="utf-8") as f:
                words_txt_lines = f.readlines()
        return words_txt_lines

    def _parse_lines(self, lines):
        """
        :param lines: list of str; lines from words.txt
        - these lines indicate either mode changes or transformations
        - this method parses the lines and returns a data structure which
          informs the transformer of how to behave
        :return: TRDefinitions
        """
        all_modes = frozenset([TRParseMode.ANY,
                               TRParseMode.SPEC,
                               TRParseMode.EXTRA,
                               TRParseMode.DEFAULT,
                               TRParseMode.NOT_SPECS])
        specs = {}
        extras = {}
        defaults = {}
        mode = TRParseMode.ANY

        for line in lines:
            line = line.strip()
            # ignore comments and empty lines
            if line.startswith("#") or line.isspace():
                continue
            # handle mode changes
            if line in all_modes:
                mode = line
                continue
            # ignore invalid lines (not a mode, not a transformation)
            if "->" not in line:
                continue

            # extract source and target
            source_and_target = line.split("->")
            source = source_and_target[0].strip()
            # allow for inline comments on the right side of the line
            target = "#".join(source_and_target[1].split("#")[:1])
            target = target.strip()

            """
            See TRParseMode notes for what the different modes mean.
            These three dicts represent locations to replace text in
            a rule.
            """
            if mode == TRParseMode.ANY:
                specs[source] = target
                extras[source] = target
                defaults[source] = target
            elif mode == TRParseMode.SPEC:
                specs[source] = target
            elif mode == TRParseMode.EXTRA:
                extras[source] = target
            elif mode == TRParseMode.DEFAULT:
                defaults[source] = target
            elif mode == TRParseMode.NOT_SPECS:
                extras[source] = target
                defaults[source] = target

        return TRDefinitions(specs, extras, defaults)
