import logging
import lxml
import openpyxl
import os

from  constants import (
    DEF_LOG_LEVEL, DEF_SFX, LANG_ROW, START_COL, START_ROW, XML_ATTR_STR_NAME,
    XML_TAG_ROOT, XML_TAG_STR, KEY_COL
)

class AppLangTranslate:
    suffix = DEF_SFX

    def _is_readable_file(self, path):
        return os.path.isfile( path ) and os.access( path, os.R_OK )

    def _out_file_name(self, lang, xml=True):
        return lang.lower().replace( ' ', '-' ) + '-' + DEF_SFX + \
            ('.xml' if xml else '.txt')

    def __init__(
            self, path, start_col=START_COL, end_col=0, start_row=START_ROW,
            end_row=0, lang_row=LANG_ROW, stop_on_null=True, stop_on_err=False
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

        self.lang_row = lang_row

        self.stop_on_null = stop_on_null
        self.stop_on_err = stop_on_err

        self._set_log_level( DEF_LOG_LEVEL  )

        msg = 'Reading from: "{}". Settings are:\n'
        '\tCols={}.{}'
        '\tRows={},{},\n'
        '\tlang. row={}\n'.format(
            self.path, self.start_col, self.end_col, self.start_row,
            self.end_row, self.lang_row
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

    def _col_to_txt(self, column):
        """
        Writes translated strings from one column to text

        column: numeric index ofcolumn
        """
        cell = self.ws.cell( column=column, row=self.lang_row )
        if not cell.value:
            msg = 'Missing language name at col. "{}", row "{}"'.format(
                column, self.lang_row
            )
            logging.error( msg )
            raise ValueError( msg )

        path = self._out_file_name( cell.value, xml=False )

        with open( path, 'w' ) as foutp: 
            for i, row in enumerate(
                    range( self.start_row, self.ws.max_row + 1 ), 1
            ): 
                cell = self.ws.cell( column=column, row=row ) 

                if self.stop_on_null:
                    cell_2 = self.ws.cell( column=2, row=row )
                    cell_6 = self.ws.cell( column=6, row=row )
                    if cell_2.value is None and cell_6.value is None: 
                        break

                foutp.write( (cell.value or '') + '\n' )

        logging.info(
            'Wrote {} strings in col. {} to text for "{}" for language '
            '"{}"'.format(
                i, openpyxl.utils.cell.get_column_letter( column ), path,
                cell.value
            )
        )

    def _col_to_xml(self, column):
        """
        Writes translated strings from one column to XML

        column: numeric index ofcolumn
        """
        cell = self.ws.cell( column=column, row=self.lang_row )
        if not cell.value:
            msg = 'Missing language name at col. "{}", row "{}"'.format(
                column, self.lang_row
            )
            logging.error( msg )
            raise ValueError( msg )

        path = self._out_file_name( cell.value )

        root = lxml.etree.Element( XML_TAG_ROOT )
        for i, row in enumerate(
                range( self.start_row, self.ws.max_row + 1 ), 1
        ): 
            cell = self.ws.cell( column=column, row=row ) 

            if self.stop_on_null:
                cell_2 = self.ws.cell( column=2, row=row )
                cell_6 = self.ws.cell( column=6, row=row )
                if cell_2.value is None and cell_6.value is None: 
                    break

                name = self.ws.cell( column=KEY_COL, row=row ).value or ''
                child = lxml.etree.SubElement( root, XML_TAG_STR, name=name )
                child.text = cell.value or ''

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

    def to_xml(self, xml=True):
        """
        Writes output test files files
        """
        try:
            self.wb = openpyxl.load_workbook( self.path )
            self.ws = self.wb.active

            self._check_limits()
        except Exception as e:
            logging.error(
                'Exception in initialising processing. {}:{}'.format(
                    e.__class__.__name__, e
                )
            )
            raise

        for col in range( self.start_col, self.end_col + 1 ):
            try:
                if xml:
                    self._col_to_xml( col )
                else:
                    # Text
                    self._col_to_txt( col )
            except ValueError as e:
                logging.error(
                    'Exception in processing. col {}  {}:{}'.format(
                        openpyxl.utils.cell.get_column_letter( col ),
                        e.__class__.__name__, e
                    )
                )
                if self.stop_on_err:
                    raise

    def to_txt(self):
        try:
            self.to_xml( xml=False )
        except Exception:
            raise
