# Starting row index: name of language in local srript is in this row
START_ROW = 3

# Starting column index: this is the "English" column
START_COL = 6

# Column containing keys
KEY_COL = 1

# Row containing language names in English
LANG_ROW = 1

# Default suffix foroutput files. Output files are named <lang>-<sfx>.xml,
# where "lang" is the English-language name of the language given in the first
# row (lowercase, and with intermediate spaces replaced by hyphens),
# e.g., chinese-simplified-strings.xml
DEF_SFX = 'strings'

# Level names in  the "logging" module
LOG_LEVELS = ('WARNING', 'INFO', 'DEBUG', 'ERROR', 'CRITICAL',) 
# Default logging level in the "logging" module
DEF_LOG_LEVEL = 'ERROR'

# XML tag names
XML_TAG_ROOT = 'resources'
XML_TAG_STR = 'string'
XML_ATTR_STR_NAME = "name"
