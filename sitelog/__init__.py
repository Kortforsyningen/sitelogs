import re

def _determine_line_type(line):
    if line.strip() == '':
        line_type = 'blank'
    elif re.match(r'^\d{1,2}\.\s', line):
        line_type = 'sectionheader'
    elif re.match(r'^\d{1,2}\.[\dx]{1,2}\s', line):
        line_type = 'subsectionheader'
    elif re.match(r'^\d{1,2}\.\d{1,2}\.[\dx]{1,2}\s', line):
        line_type = 'subsubsectionheader'
    elif re.match(r'^\s+.*\s:\s.+$', line):
        if re.match(r'^\s*:\s.*$', line):
            line_type = 'key_value_continued'
        elif re.match(r'^\s+[\S ]+\s:\s+$', line):
            line_type = 'key_value_empty'
        else:
            line_type = 'key_value'
    else:
        line_type = 'freeform'

    return line_type

from .sitelogger import SiteLog
