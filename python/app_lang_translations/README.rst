Instructions to install requirements, run tests, and use. Python 3.x is needed.

* Setup

  * Create the virtual environment::

      python3 -m venv env

   Activate it::

     source ./bin/env/activate

   Check that one is indeed inside the virtual environment. This command should show you python in env/bin::

     which python

  * Install requirements inside the virtual environment::

    pip install -install/r requirements.txt

* Run tests::

    python tests/test_app_lang_translate.py
    python tests/test_xml2json.py

* Convert Excel to Android / iOS language files::

    # See usage message
    python app_lang_translate.py -h

    # Convert a .xlsx file in the format used by HelpinOut; the columns in the
    # Excel containing the translated strings for a given language. Two .zip
    # files are created:
    # 1. Android: android_languages.zip which contains directories in the
    #    Android language translations format, e.g.,
    #    values/strings.xml     # For English
    #    values-hi/strings.xml  # For Hindi
    #    ...
    #
    # 2. iOS: ios_labguages.zip which contain files, e.g.,
    #    hi.json  # For Hindi
    #    mr.json  # For Marathi
    python app_lang_translate.py <xlsx input file>
    
* Convert Android XML language files to iOS JSON format::

    # The Android XML files can be one of:
    # 1. A single XML file in a sub-directory, e.g., values-mr/strings.xml, which is the usual format
    # 2. A .zip file with multiple XML files in a hierarchy as above, e.g., the .zip file contains:
    #         values-hi/strings.xml
    #         values-mr/strings.xml
    #         ...
    #    This is the output format produced by app_lang_translate.py
    # 3. A single XML file where the language name is directly in the filename, e.g., mr.xml. This is just for convenience
    #
    # Multiple files can be specified on the command-line. For each input file,
    # the output iOS JSON file is named <lang>.json, e.g., hi.json
    #
    # The following command, with langs.zip containing:
    #     values-or/strings.xml
    #     values-kn/strings.xml
    # would produce the output iOS JSON files, mr.json, hi.json, or.json, and
    # kn.json. By default, these would be inside a .zip file, ios_languages.zip
    python xmls2json.py mr.xml values-hi/strings.xml langs.zip

