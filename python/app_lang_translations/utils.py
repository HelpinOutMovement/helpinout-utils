import json
import logging
import lxml
import openpyxl
import os
import shutil
import zipfile
try:
    import zlib
    COMPRESSION = zipfile.ZIP_DEFLATED
except:
    COMPRESSION = zipfile.ZIP_STORED

from  constants import (
    DEF_LOG_LEVEL, DEF_SFX, ENGLISH_COL, JSON_LANG_ROW, JSON_LOCALE_FILE_NAME,
    JSON_ZIP_FILE_NAME, START_COL, START_ROW, XML_ATTR_STR_NAME,
    XML_CDATA_COL, XML_KEY_COL, XML_LANG_FILE_NAME, XML_LANG_ROW,
    XML_LANG_ENGLISH_CODE, XML_TAG_ROOT, XML_TAG_STR, XML_TRANS_COL,
    XML_ZIP_FILE_NAME
)

ZIPFIle_MODES = {
    zipfile.ZIP_DEFLATED: 'deflated',
    zipfile.ZIP_STORED:   'stored',
}

class AppLangTranslate:
    suffix = DEF_SFX

    def _is_writable_dir(self, path):
        return os.path.isdir( path ) and os.access( path, os.W_OK )

    def _is_readable_file(self, path):
        return os.path.isfile( path ) and os.access( path, os.R_OK )

    def _out_json_file_name(self, lang):
        return lang.lower() + '.json'

    def _out_xml_file_name(self, lang):
        return lang.lower(), XML_LANG_FILE_NAME

    def __init__(
            self, path, start_col=START_COL, end_col=0, start_row=START_ROW,
            end_row=0, json_lang_row=JSON_LANG_ROW, xml_lang_row=XML_LANG_ROW,
            english_col=ENGLISH_COL, xml_cdata_col=XML_CDATA_COL,
            xml_key_col=XML_KEY_COL, xml_trans_col=XML_TRANS_COL,
            stop_on_null=True, stop_on_err=False, filesystem=False
    ):
        """
        path: .xlsx file path. Input file in HelpinOut format
        start_col: starting column
        end_col: Ending column. Zero means last column
        start_row: starting row
        end_row: Ending row. Zero means last row
        stop_on_bn_null: if True, output stops at first cellentry that is None.
             This is needef because the HelpinOut Excel has blankrows at the
             end.
        stop_on_err: if True,processing stops if there is an error in any col.
        """
        if not self._is_readable_file( path ):
            msg = '"{} is not a readable file'.format( path )
            logging.error( msg )
            raise ValueError( msg )

        self.path = path

        self.start_col = start_col
        self.end_col = end_col

        self.start_row = start_row
        self.end_row = end_row

        self.json_lang_row = json_lang_row
        self.xml_lang_row = xml_lang_row

        self.english_col = english_col

        self.xml_key_col = xml_key_col
        self.xml_cdata_col = xml_cdata_col
        self.xml_trans_col = xml_trans_col

        self.stop_on_null = stop_on_null
        self.stop_on_err = stop_on_err

        self.filesystem = filesystem

        self._set_log_level( DEF_LOG_LEVEL  )

        msg = 'Reading from: "{}". Settings are:\n'
        '\tCols={}.{}'
        '\tRows={},{},\n'
        '\tJSON lang. rows={}\n'
        '\tXML lang. rows={}\n'.format(
            self.path, self.start_col, self.end_col, self.start_row,
            self.end_row, self.json_lang_row, self.xml_lang_row
        )
        logging.info( msg )

    def _set_log_level(self, level):
        """
        sets the log levelin the configuration for the "logging" module.
        """
        val = getattr( logging, level.upper(), None )
        if val is None:
            raise ValueError( 'Invalid log level "{}"'.format( level ) )

        logging.info( 'Setting log. level to: "{}" ({})'.format( level, val ) )
        logging.basicConfig( level=val )

    def set_log_level(self, level):
        """
        Public method to sey logging level.

        level: string defining level as per the "logging" module. One of
               "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        """
        self._set_log_level( level )

    def _cdata(self, txt):
        """
        Wraps text in CDATA tags

        txtL text of entry
        """
        return '![CDATA[{}]]'.format( txt.replace( '\n', '<br/>' ) )

    def _col_to_json(self, column, locale_codes, locale_names, zoutp=None):
        """
        Writes translated strings from one column to JSON

        column: numeric index ofcolumn
        zoutp: either None, or a zipfile.ZipFile object. If None, the file is
               written directly to the file system
        locale_codes: locale codes from "locale.json"
        locale_names: locale names from "locale.json". Matchs one-to-one with
               locale_codes
        """
        lang = self.ws.cell( column=column, row=self.json_lang_row )
        if lang.value:
            try:
                idx = locale_codes.index( lang.value )
                locale_name = locale_names[idx]
            except ValueError as e:
                msg - 'Unable to find "{}" in locale code, or an issue in '
                'finding the locale name in locale file "{}"'.format(
                    lang.value, JSON_LOCALE_FINE_NAME
                )
        else:
            msg = 'Missing language name at col. "{}", row "{}"'.format(
                column, self.json_lang_row
            )
            logging.error( msg )
            raise ValueError( msg )

        data = { 'Locale_Code': locale_name } 

        for i, row in enumerate(
                range( self.start_row, self.ws.max_row + 1 ), 1
        ):
            name = self.ws.cell(
                column=self.xml_key_col, row=row
            ).value or ''
            if self.stop_on_null and not name:
                break

            english =  self.ws.cell( column=self.english_col, row=row )
            if english.value is not None:
                cell = self.ws.cell( column=column, row=row ) 
                key = english.value.replace( '.', '' )
                data[key] = cell.value or english.value

        try:
            path = self._out_json_file_name( lang.value )
        except OSError:
            raise

        with open( path, 'wb' ) as foutp:
            foutp.write(
                json.dumps( data, indent=4, ensure_ascii=False ).encode(
                    'utf-8'
                )
            )

        logging.info(
            'Wrote {} strings in col. {} to JSOB for "{}" for language '
            '"{}"'.format(
                i, openpyxl.utils.cell.get_column_letter( column ), path,
                cell.value
            )
        )

        if zoutp is not None:
            zoutp.write( path )

            try:
                os.unlink( path )
            except OSError as e:
                logger.warn(
                    'Error in deleting JSON file, "{}", after adding it to '
                    ''.format( path, zoutp.filename )
                )

    def _col_to_xml(self, column, zoutp=None):
        """
        Writes translated strings from one column to XML

        column: numeric index ofcolumn
        zoutp: either None, or a zipfile.ZipFile object. If None, the file is
               written directly to the file system
        """
        cell = self.ws.cell( column=column, row=self.xml_lang_row )
        if not cell.value:
            msg = 'Missing language name at col. "{}", row "{}"'.format(
                column, self.xml_lang_row
            )
            logging.error( msg )
            raise ValueError( msg )

        try:
            dir, fname = self._out_xml_file_name( cell.value )

            if not self._is_writable_dir( dir ):
                os.mkdir( dir )

            path = os.path.join( dir, fname )
        except OSError:
            raise

        root = lxml.etree.Element( XML_TAG_ROOT )
        for i, row in enumerate(
                range( self.start_row, self.ws.max_row + 1 ), 1
        ):
            translatable = self.ws.cell(
                column=self.xml_trans_col, row=row
            ).value
            translatable = True if translatable is None else \
                           bool( translatable )

            if not translatable and dir != XML_LANG_ENGLISH_CODE:
                # Non-translatable strings are output only for Englis
                continue

            name = self.ws.cell(
                column=self.xml_key_col, row=row
            ).value or ''
            if self.stop_on_null and not name:
                break

            if translatable:
                child = lxml.etree.SubElement( root, XML_TAG_STR, name=name )
            else:
                # This will be written only for English: we check
                # "translayable" above, and for non-English languages,
                # continue if it is False 
                child = lxml.etree.SubElement(
                    root, XML_TAG_STR, name=name, translatable='False'
                )

            cell = self.ws.cell( column=column, row=row ) 

            cdata = self.ws.cell(
                column=self.xml_cdata_col, row=row
            ).value or ''
            if cdata == 1:  # cdata.lower() == 'yes':
                child.text = self._cdata( cell.value or '' )
            else:
                if cell.value:
                   child.text = cell.value
                else:
                    english =  self.ws.cell( column=self.english_col, row=row )
                    child.text = english.value or ''
 
        with open( path, 'wb' ) as foutp:
            foutp.write(
                lxml.etree.tostring(
                    root, pretty_print=True, encoding='utf-8'
                )
            )

        logging.info(
            'Wrote {} strings in col. {} to XML for "{}" for language '
            '"{}"'.format(
                i, openpyxl.utils.cell.get_column_letter( column ), path,
                cell.value
            )
        )

        if zoutp is not None:
            zoutp.write( path )

            shutil.rmtree( dir )

    def _check_limits(self):
        """
        Sanity check for specified rows and columns
        """
        if self.start_col < self.ws.min_column:
            msg = 'Start column "{}" is less than min. col "{}"'.format(
                self.start_col, self.ws.min_column
            )
            raise ValueError( msg )

        if self.end_col == 0:
            self.end_col = self.ws.max_column
        else:
            if self.end_col > self.ws.max_column:
                msg = 'End column "{}" is greater than min. col "{}"'.format(
                    self.end_col, self.ws.max_column
                )
                raise ValueError( msg )

        if self.start_row < self.ws.min_row:
            msg = 'Start row "{}" is less than min. row "{}"'.format(
                self.start_row, self.ws.min_row
            )
            raise ValueError( msg )

        if self.end_row == 0:
            self.end_row = self.ws.max_row
        else:
            if self.end_row > self.ws.max_row:
                msg = 'End row "{}" is greater than min. row "{}"'.format(
                    self.end_row, self.ws.max_row
                )
                raise ValueError( msg )

    def to_out(self, xml=True):
        """
        Writes output test files files

        xml: if True, XML output is produced. else JSON
        """
        try:
            self.wb = openpyxl.load_workbook( self.path )
            self.ws = self.wb.active

            self._check_limits()
        except:
            raise

        if not xml:
            # Read locale names
            if not self._is_readable_file( JSON_LOCALE_FILE_NAME ):
                msg = '"{} is not a readable file'.format(
                    JSON_LOCALE_FILE_NAME
                )
                logging.error( msg )
                raise ValueError( msg )

            with open( JSON_LOCALE_FILE_NAME, 'r' ) as finp:
                try:
                    vals = json.loads( finp.read() )

                    locale_codes = [d['code'] for d in vals]
                    locale_names = [d['name'] for d in vals]
                except ValueError:
                    raise

        if self.filesystem:
            zoutp = None
        else:
            zoutp = zipfile.ZipFile(
                XML_ZIP_FILE_NAME if xml else JSON_ZIP_FILE_NAME, mode='w'
            )

        for col in range( self.start_col, self.end_col + 1 ):
            try:
                if xml:
                    self._col_to_xml( col, zoutp=zoutp )
                else:
                    self._col_to_json(
                        col, locale_codes, locale_names, zoutp=zoutp
                    )
            except (OSError, ValueError) as e:
                logging.error(
                    'Exception in processing. col {}  {}:{}'.format(
                        openpyxl.utils.cell.get_column_letter( col ),
                        e.__class__.__name__, e
                    )
                )
                if self.stop_on_err:
                    if not self.filesystem:
                        zoutp.close()
                    raise

        if not self.filesystem:
            zoutp.close()

    to_xml = to_out

    def to_json(self):
        try:
            self.to_out( xml=False )
        except Exception:
            raise
