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

    python tests/test_csv2xml.py

* Use::

    $ See usage messahe
    python xsv2xml.py -h

    # Convert a .csv file in theformat ised by HelpinOut:
    # The first three columns are ignored, as is the fourth one with the
    # English source strings
    # For each of the other columns, a XML is created, named as the column
    # header (in lowercase, and with intermediate spaces replaced by hyphens),
    # e.g., chinese-simplified-strings.xml
    python xsv2xml.py languages.csv

    $ 
