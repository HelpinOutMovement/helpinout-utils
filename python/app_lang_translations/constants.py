# Starting row index: name of language in local srript is in this row
START_ROW = 5

# Starting column index: by default this is the "English" column
START_COL = 8

# Column index for "English"
ENGLISH_COL = 8

# Column containing keys for Amdroid XML
XML_KEY_COL = 1
# Column containing CDATA for Android XML
XML_CDATA_COL = 2
# Column containing translatable flag for Android XML
XML_TRANS_COL = 3

# Andrid places language translation files inside a directory named as per
# the language code, e.g., inside values-ji/ for Hindi. This is the name of
# the language file
XML_LANG_FILE_NAME = 'strings.xml'

# English is dealt with specially in Android (e.g., some strings are not
# translatable)
XML_LANG_ENGLISH_CODE = 'values'

# Names of output zip files
JSON_ZIP_FILE_NAME = 'ios_langages.zip'
XML_ZIP_FILE_NAME = 'android_langages.zip'

# Name of locale file for JSON, containing locale names, and codes
JSON_LOCALE_FILE_NAME = 'locale.json'

# Row containing language names in English for iOS JSON
JSON_LANG_ROW = 2
# Row containing language names in English for Android XML
XML_LANG_ROW = 3

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
