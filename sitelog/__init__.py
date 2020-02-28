import re
import textwrap


def _determine_line_type(line):
    """
    Determine which type a line is...
    """
    if line.strip() == "":
        line_type = "blank"
    elif re.match(r"^\d{1,2}\.\s", line):
        line_type = "sectionheader"
    elif re.match(r"^\d{1,2}\.[\dx]{1,2}\s", line):
        line_type = "subsectionheader"
    elif re.match(r"^\d{1,2}\.\d{1,2}\.[\dx]{1,2}\s", line):
        line_type = "subsubsectionheader"
    elif re.match(r"^\s+.*\s:\s.+$", line):
        if re.match(r"^\s*:\s.*$", line):
            line_type = "key_value_continued"
        elif re.match(r"^\s+[\S ]+\s:\s+$", line):
            line_type = "key_value_empty"
        else:
            line_type = "key_value"
    else:
        line_type = "freeform"

    return line_type


def _format_string(line, line_type):
    """
    formatting lines to sitelog format 

    options:
    "sectiontitle"
    "sectionnr"
    "subsectitle"
    "subsubsecnr"
    "subsubsectitle"
    "mainkey"
    "subkey"
    "multilinevalue"
    """
    formatted_string = ""

    if line_type == "sectiontitle":
        formatted_string = line

    if line_type == "sectionnr":
        formatted_string = "{:6}".format(line)

    if line_type == "subsectitle":
        formatted_string = "{:24}{:2}".format(line, ":")

    if line_type == "subsubsecnr":
        formatted_string = "{:6}".format(line)

    if line_type == "subsubsectitle":
        if len(line) < 23:
            formatted_string = "{:24}{:2}".format(line, ":")
        else:
            lines = textwrap.wrap(line, width=23)
            for i, l in enumerate(lines):
                if i == 0:
                    formatted_l = "{:24}{:2}".format(l, ":")
                else:
                    formatted_l = "\n{:6}{:24}{:2}".format("", l, ":")
                formatted_string += formatted_l

    if line_type == "mainkey":
        formatted_string = line.rjust(len(line) + 5)
        formatted_string = "{:30}{:2}".format(formatted_string, ":")

    if line_type == "subkey":
        formatted_string = line.rjust(len(line) + 7)
        formatted_string = "{:30}{:2}".format(formatted_string, ":")

    if line_type == "multilinevalue":
        if len(line) < 48:
            formatted_string = line
        else:
            lines = textwrap.wrap(line, width=48)
            for i, l in enumerate(lines):
                if i == 0:
                    formatted_l = l
                else:
                    formatted_l = "\n{:>31} ".format(":") + l
                formatted_string += formatted_l

    return formatted_string


from .antenna import *
from .collocation import *
from .frequencystandard import *
from .header_form import *
from .receiver import *
from .sections import *
from .siteidentification import *
from .sitelocation import *
from .sitelogger import *
from .surveyedties import *
from .meteorologicalinstruments import *
