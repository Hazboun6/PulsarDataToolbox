# -*- coding: utf-8 -*-
# encoding=utf8
"""Main module."""

#Pulsar Data Toolbox. Based on fitsio package. See https://github.com/esheldon/fitsio for details.
from __future__ import (absolute_import, division,
                    print_function, unicode_literals)
import numpy as np
import fitsio as F
import collections, os, sys
import datetime
import warnings

package_path = os.path.dirname(__file__)
template_dir = os.path.join(package_path, './templates/')

class psrfits(F.FITS):

    def __init__(self, psrfits_path, mode='rw', from_template=False,
                 obs_mode=None, verbose=True):
        """
        Class which inherits fitsio.FITS() (Python wrapper for cfitsio) class's
        functionality, and add's new functionality to easily manipulate and make
        PSRFITS files.

        Parameters
        ----------

        from_template : bool, str
            Either a boolean which dictates if a copy would like to be made from
            a template, or a string which is the path to a user chosen template.

        psrfits_path : str
            Either the path to an existing PSRFITS file or the name for a new
            file.

        obs_mode : Same as OBS_MODE in a standard PSRFITS, either SEARCH, PSR or
            CAL for search mode, fold mode or calibration mode respectively.

        mode : str, {'r', 'rw, 'READONLY' or 'READWRITE'}
            Read/Write mode.

        """
        self.verbose = verbose
        self.psrfits_path = psrfits_path
        self.obs_mode = obs_mode

        dir_path = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(psrfits_path) and not from_template and verbose:
            print('Loading PSRFITS file from path:\n'
                  '    \'{0}\'.'.format(psrfits_path))

        #TODO If user enters 'READWRITE' (or 'rw') but from_template=False then
        # the template will track the changes in the loaded file and save them
        # as using the loaded .fits as the template...
        # or (from_template==False and mode='rw')
        elif from_template:
            if os.path.exists(psrfits_path):
                os.remove(psrfits_path)
                if verbose:
                    print('Removing older PSRFITS file from path:\n'
                          '   \'{0}\'.'.format(psrfits_path))

            if isinstance(from_template, str):
                template_path = from_template
            # elif isinstance(from_template, bool):
            #     template_path = filename #Path to template...
                #TODO: Make a template that this works for
                #dir_path + '/psrfits_template_' + obs_mode.lower() + '.fits'

            if mode in ['r','READONLY']:
                raise ValueError('Can not write new PSRFITS file if '
                                 'it is initialized in write-only mode!')

            self.written = False
            self.fits_template = F.FITS(template_path, mode='r')
            if self.obs_mode is None:
                OBS = self.fits_template[0].read_header()['OBS_MODE'].strip()
                self.obs_mode = OBS
            else:
                self.obs_mode = obs_mode

            self.draft_hdrs = collections.OrderedDict()
            self.HDU_drafts = {}
            self.subint_dtype = None

            #Set the ImageHDU to be called primary.
            self.draft_hdrs['PRIMARY'] = self.fits_template[0].read_header()
            self.n_hdrs = len(self.fits_template.hdu_list)

            for ii in np.arange(1,self.n_hdrs):
                hdr_key = self.fits_template[ii].get_extname()
                self.draft_hdrs[hdr_key] = self.fits_template[ii].read_header()
                self.HDU_drafts[hdr_key] = None
            self.draft_hdr_keys = list(self.draft_hdrs.keys())

            if verbose:
                msg = 'Making new {0} mode PSRFITS file '.format(self.obs_mode)
                msg += 'using template from path:\n'
                msg += '    \'{0}\'. \n'.format(template_path)
                msg += 'Writing to path: \n    \'{0}\''.format(psrfits_path)
                print(msg)

        if sys.version_info[0]<3:
            try:
                super(psrfits, self).__init__(psrfits_path, mode = mode)
            except TypeError:
                err_msg = 'Python 2 sometimes errors when reloading in '
                err_msg += 'Jupyter Notebooks. Try reloading kernel.'
                raise TypeError(err_msg)
        else:
            super().__init__(psrfits_path, mode = mode)

        #If self.obs_mode is still None use loaded PSRFITS file
        if self.obs_mode is None and from_template:
            OBS = self.fits_template[0].read_header()['OBS_MODE'].strip()
            self.obs_mode = OBS

        if from_template and verbose:
            print('The Binary Table HDU headers will be written as '
                  'they are added\n     to the PSRFITS file.')

        elif not from_template and (mode=='rw' or mode=='READWRITE'):
            self.draft_hdrs = collections.OrderedDict()
            self.HDU_drafts = {}
            #Set the ImageHDU to be called primary.
            self.draft_hdrs['PRIMARY'] = self[0].read_header()
            self.n_hdrs = len(self.hdu_list)
            self.written = False
            for ii in range(self.n_hdrs-1):
                hdr_key = self[ii+1].get_extname()
                self.draft_hdrs[hdr_key] = self[ii+1].read_header()
                self.HDU_drafts[hdr_key] = None
            self.draft_hdr_keys = list(self.draft_hdrs.keys())


    def write_psrfits(self, HDUs=None, hdr_from_draft=True):
        """
        Function that takes the template headers and a dictionary of recarrays
            to make into PSRFITS HDU's. These should only include BinTable HDU
            Extensions, not the PRIMARY header (an ImageHDU). PRIMARY is dealt
            with a bit differently.

        Parameters
        ----------

        HDUs : dict, optional
            Dictionary of recarrays to make into HDUs. Default is set to
            HDU_drafts
        """
        if self.written:
            raise ValueError('PSRFITS file has already been written. '
                             'Can not write twice.')
        if HDUs is None:
            HDUs = self.HDU_drafts

        if any([val is None for val in HDUs.values()]):
            raise ValueError('One of HDU drafts is \"None\".')

        self.write_PrimaryHDU_info_dict(self.fits_template[0],self[0])
        self.set_hdr_from_draft('PRIMARY')
        for hdr in self.draft_hdr_keys[1:]:
            self.write_table(HDUs[hdr],extname=hdr, extver=1)
                             # header = self.draft_hdrs[hdr])
            if hdr_from_draft: self.set_hdr_from_draft(hdr)
        self.written = True

    # def write_psrfits_from_draft?(self):
    #     self.write_PrimaryHDU_info_dict(self.fits_template[0],self[0])
    #     self.set_hdr_from_draft('PRIMARY')
    #     #Might need to go into for loop if not true for all BinTables
    #     nrows = self.draft_hdrs['SUBINT']['NAXIS2']
    #     for jj, hdr in enumerate(self.draft_hdr_keys[1:]):
    #         HDU_dtype_list = self.get_HDU_dtypes(self.fits_template[jj+1])
    #         rec_array = self.make_HDU_rec_array(nrows, HDU_dtype_list)
    #         self.write_table(rec_array)
    #         self.set_hdr_from_draft(hdr)

    # def append_subint_array(self,table):
    #     """
    #     Method to append more subintegrations to a PSRFITS file from Python
    #      arrays.
    #     The array must match the columns (in the numpy.recarray sense)
    #      of the existing PSRFITS file.
    #     """
    #     fits_to_append = F.FITS(table)

    def append_from_file(self,path,table='all'):
        """
        Method to append more subintegrations to a PSRFITS file from other
        PSRFITS files.
        Note: Tables are appended directly to the original file. Make a copy
            before copying if you are unsure about appending. The array must
            match the columns (in the numpy.recarray sense) of the existing
            PSRFITS file.

        Parameters
        ----------

        path : str
            Path to the new PSRFITS file to be appended.

        table : list
            List of BinTable HDU headers to append from file. Defaults to
                appending all secondary BinTables.
                ['HISTORY','PSRPARAM','POLYCO','SUBINT']
        """
        PF2A = F.FITS(path, mode='r')
        PF2A_hdrs = []
        PF2A_hdrs.append('PRIMARY')
        for ii in range(self.n_hdrs-1):
            hdr_key = PF2A[ii+1].get_extname()
            PF2A_hdrs.append(hdr_key)
        if table=='all':
            if PF2A_hdrs!= self.draft_hdr_keys:
                if len(PF2A_hdrs)!= self.n_hdrs:
                    err_msg = '{0} and {1} do '.format(self.psrfits_path,path)
                    err_msg += 'not have the same number of BinTable HDUs.'
                    raise ValueError(err_msg)
                else:
                    err_msg = 'Original PSRFITS HDUs'
                    err_msg = ' ({0}) and PSRFITS'.format(self.draft_hdr_keys)
                    err_msg = ' to append ({1})'.format(PF2A_hdrs)
                    err_msg = ' have different BinTables or they are in'
                    err_msg = ' different orders. \nEnter a table list matching'
                    err_msg = ' the order of the orginal PSRFITS file.'
                    raise ValueError(err_msg)
            else:
                table=PF2A_hdrs
        for hdr in self.draft_hdr_keys[1:]:
            rec_array = PF2A[list_arg(table,hdr)].read()
            self[list_arg(self.draft_hdr_keys,hdr)].append(rec_array)

#######Convenience Functions################
    def get_colnames():
        """Returns the names of all of the columns of data needed for a PSRFITS
        file."""
        return self[1].get_colnames()

    def set_hdr_from_draft(self, hdr):
        """Sets a header of the PSRFITS file using the draft header derived from
        template."""
        keys = self.draft_hdr_keys
        if isinstance(hdr,int):
            hdr_name = keys[hdr]
        if isinstance(hdr,str):
            hdr_name = hdr.upper()
            hdr = list_arg(keys,hdr_name)
        # with warnings.catch_warnings(): #This is very Dangerous
        #     warnings.simplefilter("ignore")
        for card in self.draft_hdrs[hdr_name].records():
            card = convert2asciii(card)
        self[hdr].write_keys(self.draft_hdrs[hdr_name],clean=False)
        #Must set clean to False or the first keys are deleted!

    def get_FITS_card_dict(self, hdr, name):
        """
        Make a FITS card compatible dictionary from a template FITS header that
        matches the input name key in a standard FITS card/record. It is
        necessary to make a new FITS card/record to change values in the header.
        This function outputs a writeable dictionary which can then be used to
        change the value in the header using the hdr.add_record() method.

        Parameters
        ----------

        hdr : fitsio.fitslib.FITSHDR object
            Template for the card.

        name : str
            The name key in the FITS record you wish to make.
        """
        card = next((item for item in hdr.records()
                    if item['name'] == name.upper()), False)
        if not card:
            err_msg = 'A FITS card named '
            err_msg += '{0} does not exist in this HDU.'.format(name)
            raise ValueError(err_msg)
        return card

    def make_FITS_card(self, hdr, name, new_value):
        """
        Make a new FITS card/record using a FITS header as a template.
        This function makes a new card by finding the card/record in the
        template with the same name and replacing the value with new_value.
        Note: fitsio will set the dtype dependent on the form of the new_value
        for numbers.

        Parameters
        ----------

        hdr : fitsio.fitslib.FITSHDR
            A fitsio.fitslib.FITSHDR object, which acts as the template.

        name : str
            A string that matches the name key in the FITS record you wish to
            make.

        new_value : str, float
            The new value you would like to replace.
        """
        record = self.get_FITS_card_dict(hdr,name)
        record_value = record['value']
        dtype = record['dtype']

        string_dtypes = ['C']
        number_dtypes = ['I','F']

        def _fits_format(new_value,record_value):
            """
            Take in the new_value and record value, and format for searching
            card string. Change the shape of the string to fill out PSRFITS
            File Correctly.
            """
            try: #when new_value is a string
                if len(new_value)<=len(record_value):
                    str_len = len(record_value)
                    new_value = new_value.ljust(str_len)
                card_string = record['card_string'].replace(record_value,
                                                            new_value)

            except TypeError: # When new_value is a number
                old_val_str = str(record_value)
                old_str_len = len(old_val_str)
                new_value = str(new_value)
                new_str_len = len(new_value)
                if new_str_len < old_str_len:
                    # If new value is shorter fill out with spaces.
                    new_value = new_value.rjust(old_str_len)
                elif new_str_len > old_str_len:
                    if new_str_len>20:
                        new_value=new_value[:20]
                        new_str_len = 20

                    # If new value is longer pull out more spaces.
                    old_val_str = old_val_str.rjust(new_str_len)
                card_string = record['card_string'].replace(old_val_str,
                                                            new_value)
            return card_string

        def _replace_center_of_cardstring(new_value):
            """
            Replaces the entire center of the card string using the new value.
            """
            cardstring = record['card_string']
            equal_idx = old_cardstring.find('=')
            slash_idx = old_cardstring.find('/')
            len_center = slash_idx - equal_idx - 1
            new_center = str(new_value).rjust(len_center)
            cardstring[equal_idx+1, slash_idx] = new_center
            return cardstring

        #if isinstance(record['value'],tuple):
        #    record['value'] = str(record['value']).replace(' ','')
        # for TDIM17, TDIM20 in SUBINT HDU...
        # Could make more specific if necessary.
        special_fields = ['TDIM17','TDIM20']

        if record['name'] in special_fields:
            new_record = record
            record_value = str(record_value).replace(' ','')
            card_string = _fits_format(new_value.replace(' ',''), record_value)
            new_record['card_string'] = card_string.replace('\' (','\'(')
            new_record['value'] = new_value
            new_record['value_orig'] = new_record['value']

        #TODO Add error checking new value... and isinstance(new_value)
        #Usual Case
        elif str(record['value']) in record['card_string']:
            card_string = _fits_format(new_value, record_value)
            new_record = F.FITSRecord(card_string)

        #Special Case 1, Find Numbers with trailing zeros and writes string.
        elif ((str(record['value'])[-1]=='0')
              and (str(record['value'])[:-1] in record['card_string'])):

            record_value = str(record['value'])[:-1]
            #Adds decimal pt to end of string.
            if record_value[-1]=='.' and str(new_value)[-1]!='.':
                new_value = str(new_value) + '.'
            card_string = _fits_format(new_value, record_value)
            new_record = F.FITSRecord(card_string)

        #Special Case 2, Find Numbers with upper/lower E in sci notation
        #that do not match exactly. Always use E in card string.
        elif (('dtype' in record.keys())
              and (record['dtype'] in number_dtypes)
              and (('E' in str(record_value)) or ('e' in str(record_value))
                    or ('E' in str(record['value_orig']))
                    or ('e' in str(record['value_orig'])))):

            new_value = str(new_value).upper()
            if str(record_value).upper() in record['card_string']:
                record_value = str(record_value).upper()
                card_string = _fits_format(new_value, record_value)
                new_record = F.FITSRecord(card_string)
            elif str(record_value).lower() in record['card_string']:
                record_value =str(record_value).lower()
                card_string = _fits_format(new_value, record_value)
                new_record = F.FITSRecord(card_string)
            else:
                card_string = _replace_center_of_cardstring(new_value)
                new_record = F.FITSRecord(card_string)
                msg = 'Old value cannot be found in card string. '
                msg += 'Entire center replaced.'
                print(msg)

        #Replace whole center if can't find value.
        else:
            card_string = _replace_center_of_cardstring(new_value)
            new_record = F.FITSRecord(card_string)
            msg = 'Old value cannot be found in card string. '
            msg += 'Entire center replaced.'
            print(msg)

        if new_record['value'] != new_record['value_orig']:
            new_record['value_orig'] = new_record['value']

        return new_record

    def replace_FITS_Record(self, hdr, name, new_value):
        """
        Replace a Fits record with a new value in a fitsio.fitslib.FITSHDR
        object.

        Parameters
        ----------

        hdr : str or FITSHDR object
            Header name.

        name : FITS Record/Car
            FITS Record/Card name to replace.

        new_value : float, str
            The new value of the parameter.
        """
        # try:
        #     new_record = self.make_FITS_card(hdr,name,new_value)
        # except AttributeError:
        #
        #     new_record = self.make_FITS_card(hdr,name,new_value)
        if not isinstance(hdr,F.fitslib.FITSHDR):
            hdr = self.draft_hdrs[hdr]
             #Maybe faster if try: except: used?
        new_record = self.make_FITS_card(hdr,name,new_value)
        hdr.add_record(new_record)

    def get_HDU_dtypes(self, HDU):
        """
        Returns a list of data types and array sizes needed to make a recarray.
        HDU = A FITS HDU.
        """
        return HDU.get_rec_dtype()[0].descr

    def set_HDU_array_shape_and_dtype(self, HDU_dtype_list, name,
                                      new_array_shape=None, new_dtype=None):
        """
        Takes a list of data types (output of get_HDU_dtypes()) and returns new
        list with the named element's array shape and/or data type edited.

        Parameters
        ----------

        HDU_dtype_list :
            dtype list for making recarray (output of get_HDU_dtypes()).

        name : str
            Name of parameter to edit.

        new_array_shape : tuple
            New array shape. Note 1-d arrays are of type (n,) in FITS files.

        new_dtype :
            New data type. See PSRFITS and fitsio documentation for recognized
            names.
        """
        try:
            ii = [x for x, y in enumerate(HDU_dtype_list)
                  if y[0] == name.upper()][0]
        except:
            err_msg = 'The name \'{0}\' is not '.format(name)
            err_msg += 'in the given HDU dtype list.'
            raise ValueError(err_msg)

        if new_dtype and new_array_shape:
            HDU_dtype_list[ii] = (HDU_dtype_list[ii][0],new_dtype,
                                  new_array_shape)
        elif new_array_shape:
            HDU_dtype_list[ii] = (HDU_dtype_list[ii][0],HDU_dtype_list[ii][1],
                                  new_array_shape)
        elif new_dtype:
            HDU_dtype_list[ii] = (HDU_dtype_list[ii][0],new_dtype,
                                  HDU_dtype_list[ii][2])

    def make_HDU_rec_array(self, nrows, HDU_dtype_list):
        """
        Makes a rec array with the set number of rows and data structure
        dictated by the dtype list.
        """
        #TODO Add in hdf5 type file format for large arrays?
        return np.empty(nrows, dtype=HDU_dtype_list)

    def write_PrimaryHDU_info_dict(self, ImHDU_template, new_ImHDU):
        """
        Writes the information dictionary for a primary header Image HDU
        (new_ImHDU) using ImHDU_template as the template. Both are FITS HDUs.

        Parameters
        ----------
        ImHDU_template :
            Template header.

        new_ImHDU :
            Header where template is copied.
        """
        templ_info_keys = list(ImHDU_template.__dict__['_info'].keys())
        new_info_keys = list(new_ImHDU.__dict__['_info'].keys())
        info_keys = np.unique(np.concatenate((templ_info_keys,new_info_keys)))

        for key in info_keys:
            if key in templ_info_keys:
                new_ImHDU.__dict__['_info'][key] = ImHDU_template.__dict__['_info'][key]
            elif key not in templ_info_keys:
                new_ImHDU.__dict__['_info'].__delitem__(key)

    def set_subint_dims(self, nbin=1, nchan=2048, npol=4, nsblk=4096,
                        nsubint=4, obs_mode=None, data_dtype='|u1'):
        """
        Method to set the appropriate parameters for the SUBINT BinTable of
            a PSRFITS file of the given dimensions.
        The parameters above are defined in the PSRFITS literature.
        The method automatically changes all the header information in the
            template dependent on these values. The header template is set to
            these values.
        A list version of a dtype array is made which has all the info needed
          to make a SUBINT recarray. This can then be written to a PSRFITS file,
          using the command write_prsfits().

        Parameters
        ----------

        nbin : int
            NBIN, number of bins. 1 for SEARCH mode data.

        nchan : int
            NCHAN, number of frequency channels.

        npol : int
            NPOL, number of polarization channels.

        nsblk : int
            NSBLK, size of the data chunks for search mode data. Set to 1 for
            PSR and CAL mode.

        nsubint : int
            NSUBINT or NAXIS2 . This is the number of rows or subintegrations
            in the PSRFITS file.

        obs_mode : str , {'SEARCH', 'PSR', 'CAL'}
            Observation mode.

        data_type : str
            Data type of the DATA array ('|u1'=int8 or '|u2'=int16).
        """
        self.nrows = self.nsubint = nsubint
        #Make a dtype list with defined dimensions and data type
        self._bytes_per_datum = np.dtype(data_dtype).itemsize

        if obs_mode is None: obs_mode = self.obs_mode

        if obs_mode.upper() == 'SEARCH':
            self.subint_idx = self.draft_hdr_keys.index('SUBINT')
            if nbin != 1:
                err_msg = 'NBIN (set to {0}) parameter not set '.format(nbin)
                err_msg += 'to correct value for SEARCH mode.'
                raise ValueError(err_msg)

            self.nbits = 8 * self._bytes_per_datum
            #Set Header values dependent on data shape
            self.replace_FITS_Record('PRIMARY','BITPIX',8)
            self.replace_FITS_Record('SUBINT','BITPIX',8)
            self.replace_FITS_Record('SUBINT','NBITS',self.nbits)
            self.replace_FITS_Record('SUBINT','NBIN',nbin)
            self.replace_FITS_Record('SUBINT','NCHAN',nchan)
            self.replace_FITS_Record('PRIMARY','OBSNCHAN',nchan)
            self.replace_FITS_Record('SUBINT','NPOL',npol)
            self.replace_FITS_Record('SUBINT','NSBLK',nsblk)
            self.replace_FITS_Record('SUBINT','NAXIS2',nsubint)
            self.replace_FITS_Record('SUBINT','TFORM13',str(nchan)+'E')
            self.replace_FITS_Record('SUBINT','TFORM14',str(nchan)+'E')
            self.replace_FITS_Record('SUBINT','TFORM15',str(nchan*npol)+'E')
            self.replace_FITS_Record('SUBINT','TFORM16',str(nchan*npol)+'E')

            #Calculate Number of Bytes in each row's DATA array
            tform17 = nbin*nchan*npol*nsblk
            self.replace_FITS_Record('SUBINT','TFORM17',str(tform17)+'B')

            #This is the number of bytes in TSUBINT, OFFS_SUB, LST_SUB, etc.
            bytes_in_lone_floats = 7*8 + 5*4

            naxis1 = tform17*self._bytes_per_datum + 2*nchan*4 + 2*nchan*npol*4
            naxis1 += bytes_in_lone_floats
            self.replace_FITS_Record('SUBINT','NAXIS1', str(naxis1))

            # Set the TDIM17 string-tuple
            tdim17 = '('+str(nbin)+', '+str(nchan)+', '
            tdim17 += str(npol)+', '+str(nsblk)+')'
            self.replace_FITS_Record('SUBINT','TDIM17', tdim17)

            self.subint_dtype = self.get_HDU_dtypes(self.fits_template
                                                    [self.subint_idx])
            self.set_HDU_array_shape_and_dtype(self.subint_dtype,'DATA',
                                               (nbin,nchan,npol,nsblk))
                                               #,data_dtype)

            self.single_subint_floats=['TSUBINT','OFFS_SUB',
                                       'LST_SUB','RA_SUB',
                                       'DEC_SUB','GLON_SUB',
                                       'GLAT_SUB','FD_ANG',
                                       'POS_ANG','PAR_ANG',
                                       'TEL_AZ','TEL_ZEN']

        elif (obs_mode.upper() == 'PSR' or obs_mode.upper() == 'CAL'):
            self.subint_idx = self.draft_hdr_keys.index('SUBINT')
            if nsblk != 1:
                err_msg = 'NSBLK (set to {0}) parameter not set '.format(nsblk)
                err_msg += 'to correct value '
                err_msg += 'for {0} mode.'.format(obs_mode.upper())
                raise ValueError(err_msg)

            self.nbits = 1
            self.replace_FITS_Record('PRIMARY','BITPIX',8)
            self.replace_FITS_Record('SUBINT','BITPIX',8)
            self.replace_FITS_Record('SUBINT','NBITS',self.nbits)
            self.replace_FITS_Record('SUBINT','NBIN',nbin)
            self.replace_FITS_Record('SUBINT','NCHAN',nchan)
            self.replace_FITS_Record('PRIMARY','OBSNCHAN',nchan)
            self.replace_FITS_Record('SUBINT','NPOL',npol)
            self.replace_FITS_Record('SUBINT','NSBLK',nsblk)
            self.replace_FITS_Record('SUBINT','NAXIS2',nsubint)
            self.replace_FITS_Record('SUBINT','TFORM16',str(nchan)+'D')
            self.replace_FITS_Record('SUBINT','TFORM17',str(nchan)+'E')
            self.replace_FITS_Record('SUBINT','TFORM18',str(nchan*npol)+'E')
            self.replace_FITS_Record('SUBINT','TFORM19',str(nchan*npol)+'E')

            #Calculate Number of Bytes in each row's DATA array
            tform20 = nbin*nchan*npol
            self.replace_FITS_Record('SUBINT','TFORM20',str(tform20)+'I')
            bytes_in_lone_floats = 10*8 + 5*4

            #This is the number of bytes in TSUBINT, OFFS_SUB, LST_SUB, etc.
            naxis1 = tform20*self._bytes_per_datum + nchan*8 + nchan*4
            naxis1 += 2*nchan*npol*4 + bytes_in_lone_floats
            self.replace_FITS_Record('SUBINT','NAXIS1', str(naxis1))

            # Set the TDIM20 string-tuple
            tdim20 = '('+str(nbin)+', '+str(nchan)+', ' + str(npol)+')'
            self.replace_FITS_Record('SUBINT','TDIM20', tdim20)

            self.subint_dtype = self.get_HDU_dtypes(self.fits_template
                                                    [self.subint_idx])
            self.set_HDU_array_shape_and_dtype(self.subint_dtype,'DATA',
                                               (npol,nchan,nbin))

            self.single_subint_floats=['TSUBINT','OFFS_SUB',
                                       'LST_SUB','RA_SUB',
                                       'DEC_SUB','GLON_SUB',
                                       'GLAT_SUB','FD_ANG',
                                       'POS_ANG','PAR_ANG',
                                       'TEL_AZ','TEL_ZEN',
                                       'AUX_DM','AUX_RM']


        self.set_HDU_array_shape_and_dtype(self.subint_dtype,
                                           'DAT_FREQ',(nchan,))
        self.set_HDU_array_shape_and_dtype(self.subint_dtype,
                                           'DAT_WTS',(nchan,))
        self.set_HDU_array_shape_and_dtype(self.subint_dtype,
                                           'DAT_OFFS',(nchan*npol,))
        self.set_HDU_array_shape_and_dtype(self.subint_dtype,
                                           'DAT_SCL',(nchan*npol,))

    def copy_template_BinTable(self, ext_name, cols='all', dtypes=None):
        """
        Method to copy PSRFITS binary tables exactly. This is
            especially useful when using real PSRFITS files to make simulated
            data, i.e. if you would just like to replace the DATA arrays in the
            file with your simulated data, but keep the ancillary telescope
            information. This copies the BinTable as a numpy.recarray into the
            `HDU_drafts` dictionary.

        Parameters
        ----------

        ext_name : str, {'PRIMARY','SUBINT','HISTORY','PSRPARAM','POLYCO'}
            Binary Extension name to copy.

        cols : str or list
            Columns of the given BinTable to copy.

        dtypes : list of tuples
            Data types for numpy.recarray that will be the draft for the
            BinTable.
        """
        idx = self.draft_hdr_keys.index(ext_name)
        dtypes = self.get_HDU_dtypes(self.fits_template[idx])
        nrows = self.fits_template[idx].read_header()['NAXIS2']
        if cols=='all':
            cols = self.fits_template[idx].get_colnames()

        self.HDU_drafts[ext_name] = self.make_HDU_rec_array(nrows, dtypes)
        copy_cols = self.fits_template[idx].read(columns=cols)
        #TODO Think about how this would change for appending single rows.
        for col in cols:
            self.HDU_drafts[ext_name][col][:] = copy_cols[col][:]

        del copy_cols

    def set_draft_header(self, ext_name, hdr_dict):
        """
        Set draft header entries for the new PSRFITS file from a dictionary.

        Parameters
        ----------
        psrfits_object : pdat.psrfits
            Pulsar Data Toolbox PSRFITS object.

        ext_name : str, {'PRIMARY','SUBINT','HISTORY','PSRPARAM','POLYCO'}
            Name of the header to replace the header entries.

        hdr_dict : dict
            Dictionary of header changes to be made to the template header.
            Template header entries are kept, unless replaced by this function.
        """
        for key in hdr_dict.keys():
            self.replace_FITS_Record(ext_name,key,hdr_dict[key])

    def close(self):
        """
        Override of fitsio close method. Adds more variables to set to none.
        Close the fits file and set relevant metadata to None
        """
        if hasattr(self,'_FITS'):
            if self._FITS:
                #if self.verbose:
                #    print('PSRFITS file is closing.')
                #This call to print prevents a stack overflow.I do not know why.
                print('')
                self._FITS.close()
                self._FITS=None
        self._filename=None
        self.mode=None
        self.charmode=None
        self.intmode=None

        #TODO Write script that sets all non overlapping variables to None.
        self.HDU_drafts=None
        self.draft_hdr_keys=None
        self.draft_hdrs=None
        self.n_hdrs=None
        self.psrfits_path=None

        self.hdu_list=None
        self.hdu_map=None

    # def real_data(self):
    #     """
    #     Method that reads the DATA, DAT_SCL, DAT_OFFS and DAT_WTS together
    #         into a HDF5 file so that the real data can be used for
    #         calculations.
    #     """
    #     data = h5py.File('data.hdf5',mode=w)
    #     data = self[1].read_columns('DATA')
    #     dat_offs = self[1].read_columns('DATA_OFFS')
    #     dat_scl = self[1].read_columns('DATA_SCL')
    #     dat_wts = self[1].read_columns('DATA_OFFS')
    #     #data = DATA*DAT_SCL+DAT_OFFS


def list_arg(list_name, string):
    """Returns the index of a particular string in a list of strings."""
    return [x for x, y in enumerate(list_name) if y == string][0]

def convert2asciii(dictionary):
    """
    Changes all keys (i.e. assumes they are strings) to ASCII and
    values that are strings to ASCII. Specific to dictionaries.
    """
    return dict([(key.encode('ascii','ignore'),value.encode('ascii','ignore'))
                 if type(value) in [str,bytes] else
                 (key.encode('ascii','ignore'),value)
                 for key, value in dictionary.items()])
