# -*- coding: utf-8 -*-

"""Main module."""

#PyPSRFITS. Based on fitsio package. See https://github.com/esheldon/fitsio for details.
import numpy as np
import fitsio as F
import collections, os
import datetime
import warnings

class psrfits(F.FITS):

    def __init__(self, psrfits_path, mode = 'rw', from_template=False, obs_mode='SEARCH'):
        """
        Class which inherits fitsio.FITS() (Python wrapper for cfitsio) class's functionality,
        and add's new functionality for easily manipulate and make PSRFITS files.
        from_template= True, False or a string which is the path to a user chosen template.
        psrfits_path = Either the path to an existing PSRFITS file or the name for a new file.
        obs_mode = Same as OBS_MODE in a standard PSRFITS, either SEARCH, PSR or CAL
                    for search mode, fold mode or calibration mode.
        mode = 'r', 'rw, 'READONLY' or 'READWRITE'
        """
        self.psrfits_path = psrfits_path

        dir_path = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(psrfits_path) and not from_template:
            print('Loading PSRFITS file from path:\n\'{0}\'.'.format(psrfits_path))

        #TODO If user enters 'READWRITE' (or 'rw') but from_template=False then
        # the template will track the changes in the loaded file and save them as
        # using the loaded .fits as the template... or (from_template==False and mode='rw')
        elif from_template :
            if os.path.exists(psrfits_path):
                os.remove(psrfits_path)
                print('Removing older PSRFITS file from path \'{0}\'.'.format(psrfits_path))

            if isinstance(from_template, str):
                template_path = from_template
            else:
                template_path = filename
                #TODO: Make a template that this works for! dir_path + '/psrfits_template_' + obs_mode.lower() + '.fits'

            if mode == 'r':
                raise ValueError('Can not write new PSRFITS file if it is intialized in write-only mode!')

            self.fits_template = F.FITS(template_path, mode='r')
            self.draft_hdrs = collections.OrderedDict()
            self.draft_hdrs['PRIMARY'] = self.fits_template[0].read_header() #Set the ImageHDU to be called primary.
            self.n_hdrs = len(self.fits_template.hdu_list)

            for ii in range(self.n_hdrs-1):
                self.draft_hdrs[self.fits_template[ii+1].get_extname()] = self.fits_template[ii+1].read_header()
            self.draft_hdr_keys = list(self.draft_hdrs.keys())
            print('Making new {0} mode PSRFITS file using template from path:\n\'{1}\'. \nWriting to path \'{2}\'.'.format(obs_mode,template_path,psrfits_path))

        super(psrfits, self).__init__(psrfits_path, mode = mode)

        if from_template:
            print('The Binary Table HDU headers will be written as they are added\n\t to the PSRFITS file.')

    def write_psrfits(self):
        self.write_PrimaryHDU_info_dict(self.fits_template[0],self[0])
        self.set_hdr_from_draft('PRIMARY')
        nrows = self.draft_hdrs['SUBINT']['NAXIS2'] # Might need to go into for loop if not true for all BinTables
        for jj, hdr in enumerate(self.draft_hdr_keys[1:]):
            HDU_dtype_list = self.get_HDU_dtypes(self.fits_template[jj+1])
            rec_array = self.make_HDU_rec_array(nrows, HDU_dtype_list)
            self.write_table(rec_array)
            self.set_hdr_from_draft(hdr)

    def append_subint_array(self,table):
        """
        Method to append more subintegrations to a PSRFITS file from Python arrays.
        The array must match the columns (in the numpy.recarray sense)
         of the existing PSRFITS file.
        """
        fits_to_append = F.FITS(table)

#     def append_subint_file(self,table):
#         """
#         Method to append more subintegrations to a PSRFITS file from other PSRFITS files.
#         The array must match the columns (in the numpy.recarray sense)
#          of the existing PSRFITS file.
#         """
#         if table.shape != self[1]['DATA']:
#             raise ValueError('DATA array shapes do not have the same dimensions!!')
#     def method_to_access_data
#     def method_to_make SUBINT BinTable from data
#######Convenience Functions################
    def get_colnames():
        """Returns the names of all of the columns of data needed for a PSRFITS file."""
        return self[1].get_colnames()

    def list_arg(self, list_name, string):
        """Returns the argument of a particular string in a list of strings."""
        return [x for x, y in enumerate(list_name) if y == string][0]

    def set_hdr_from_draft(self, hdr):
        """Sets a header of the PSRFITS file using the same header as the template"""
        keys = self.draft_hdr_keys
        if isinstance(hdr,int):
            hdr_name = keys[hdr]
        if isinstance(hdr,str):
            hdr_name = hdr.upper()
            hdr = self.list_arg(keys,hdr_name)
        with warnings.catch_warnings(): #This is very Dangerous
            warnings.simplefilter("ignore")
            self[hdr].write_keys(self.draft_hdrs[hdr_name],clean=False)
            #Must set clean to False or the first keys are deleted!

    def get_FITS_card_dict(self, hdr,name):
        """
        Make a FITS card compatible dictionary from a template FITS header that matches the input name key in a standard FITS card/record.
        It is necessary to make a new FITS card/record to change values in the header.
        This function outputs a writeable dictionary which can then be used to change the value in the header using the hdr.add_record() method.
        hdr = A fitsio.fitslib.FITSHDR object, which acts as the template.
        name = A string that matches the name key in the FITS record you wish to make.
        """
        card = next((item for item in hdr.records() if item['name'] == name.upper()), False)
        if not card:
            raise ValueError('A FITS card with that name does not exist in this HDU.')
        return card

    def make_FITS_card(self, hdr,name,new_value):
        """
        Make a new FITS card/record using a FITS header as a template.
        This function makes a new card by finding the card/record in the template with the same name
        and replacing the value with new_value.
        Note: fitsio will set the dtype dependent on the form of the new_value for numbers.
        hdr = A fitsio.fitslib.FITSHDR object, which acts as the template.
        name = A string that matches the name key in the FITS record you wish to make.
        new_value = The new value you would like to replace.
        """
        record = self.get_FITS_card_dict(hdr,name)

        if isinstance(record['value'],tuple):
            record['value'] = str(record['value']).replace(' ','')
            #Workaround for TDIM17 in SUBINT HDU... Could make more specific if necessary.

        if str(record['value']) in record['card_string']: #TODO Add error checking new value... and isinstance(new_value)
            try: #when new_value is a string
                if len(new_value)<len(record['value']):
                    new_value = new_value.ljust(str_len)
                card_string = record['card_string'].replace(record['value'],new_value)
            except: # When new_value is a number
                old_val_str = str(record['value'])
                old_str_len = len(old_val_str)
                new_value = str(new_value)
                new_str_len = len(new_value)
                if new_str_len < old_str_len:
                    new_value = new_value.rjust(old_str_len) # If new value is shorter fill out with spaces.
                elif new_str_len > old_str_len:
                    old_val_str = old_val_str.rjust(new_str_len) # If new value is longer pull out more spaces.
                card_string = record['card_string'].replace(old_val_str,new_value)
        else:
            raise ValueError('The old value, {0}, does not appear in this exact form in the FITS Header.'.format(str(record['value'])))

        new_record = F.FITSRecord(card_string)
        if new_record['value'] != new_record['value_orig']:
            new_record['value_orig']=new_record['value']
        return new_record

    def replace_FITS_Record(self, hdr, name, new_value):
        if isinstance(hdr,str):
            hdr = self.draft_hdrs[hdr] #Maybe faster if try: except: used?
        new_record = self.make_FITS_card(hdr,name,new_value)
        hdr.add_record(new_record)

    def get_HDU_dtypes(self, HDU):
        return HDU.get_rec_dtype()[0].descr

    def set_HDU_array_shape_and_dtype(self, HDU_dtype_list, name, new_array_shape=None, new_dtype=None):
        try:
            ii = [x for x, y in enumerate(HDU_dtype_list) if y[0] == name.upper()][0]
        except:
            raise ValueError('The name \'{0}\' is not in the given HDU dtype list.'.format(name))
        if new_dtype and new_array_shape:
            HDU_dtype_list[ii] = (HDU_dtype_list[ii][0],new_dtype,new_array_shape)
        elif new_array_shape:
            HDU_dtype_list[ii] = (HDU_dtype_list[ii][0],HDU_dtype_list[ii][1],new_array_shape)
        elif new_dtype:
            HDU_dtype_list[ii] = (HDU_dtype_list[ii][0],new_dtype,HDU_dtype_list[ii][2])

    def make_HDU_rec_array(self, nrows, HDU_dtype_list):
        return np.empty(nrows, dtype=HDU_dtype_list)

    def write_PrimaryHDU_info_dict(self, ImHDU_template,new_ImHDU):
        try:
            new_ImHDU.__dict__['_info'].__delitem__('error')
        except:
            pass
        for key in ImHDU_template.__dict__['_info'].keys():
            if key not in new_ImHDU.__dict__['_info'].keys():
                new_ImHDU.__dict__['_info'][key] = ImHDU_template.__dict__['_info'][key]

    def set_subint_dims(self, nbin=1,nchan=2048,npol=4,nsblk=4096, nsubint=4, obs_mode='search',data_dtype='|u2'):
        """
        Method to set the appropriate parameters for a PSRFITS file of the given dimensions.
        The parameters above are defined in the PSRFITS literature.
        nbin = NBIN, number of bins. 1 for SEARCH mode data
        nchan = NCHAN, number of frequency channels
        npol = NPOL, number of polarization channels
        nsblk = NSBLK, size of the data chunks for search mode data. Set to 1 for PSR and CAL mode.
        nsubint = NSUBINT or NAXIS2 . This is the number of rows or subintegrations in the PSRFITS file.
        obs_mode = observation mode. (SEARCH, PSR, CAL)
        """
        #Checks
        if obs_mode.upper() == 'SEARCH':
            sub_int_ind = 1 #This must always be true, but worth testing..
            if nbin != 1:
                raise ValueError('NBIN (set to {0}) parameter not set to correct value for SEARCH mode.'.format(nbin))
        if (obs_mode.upper() == 'PSR' or obs_mode.upper() == 'CAL'):
            sub_int_ind = 4 #Need to check that this is always true...
            if nsblk != 1:
                raise ValueError('NSBLK (set to {0}) parameter not set to correct value for {1} mode.'.format(nsblk,obs_mode.upper()))

        if data_dtype=='|u1':
            self.bitpix = 8
        elif data_dtype=='|u2':
            self.bitpix = 16
        #Set Header values dependent on data shape
        self.replace_FITS_Record('PRIMARY','BITPIX',self.bitpix)
        self.replace_FITS_Record('SUBINT','BITPIX',self.bitpix)
        self.replace_FITS_Record('SUBINT','NBITS',self.bitpix)
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
        tform17 = nbin*nchan*npol*nsblk*self.bitpix
        self.replace_FITS_Record('SUBINT','TFORM17',str(tform17)+'B')
        bytes_in_lone_floats = 7*8 + 5*4 #This is the number of bytes in TSUBINT, etc.
        naxis1 = str(tform17 + 2*nchan*4 + 2*nchan*npol*4 + bytes_in_lone_floats)
        self.replace_FITS_Record('SUBINT','NAXIS1', str(naxis1)+'B')
        tdim17 = '('+str(nbin)+','+str(nchan)+','+str(npol)+','+str(nsblk)+')'
        self.replace_FITS_Record('SUBINT','TDIM17', tdim17)

        #Make a dtype list with defined dimensions and data type
        self.nrows = self.nsubint = nsubint
        self.subint_dtype = self.get_HDU_dtypes(self.fits_template[sub_int_ind])
        self.set_HDU_array_shape_and_dtype(self.subint_dtype,'DAT_FREQ',(nchan,))
        self.set_HDU_array_shape_and_dtype(self.subint_dtype,'DAT_WTS',(nchan,))
        self.set_HDU_array_shape_and_dtype(self.subint_dtype,'DAT_OFFS',(nchan*npol,))
        self.set_HDU_array_shape_and_dtype(self.subint_dtype,'DAT_SCL',(nchan*npol,))
        self.set_HDU_array_shape_and_dtype(self.subint_dtype,'DATA',data_dtype,(nbin,nchan,npol,nsblk))
