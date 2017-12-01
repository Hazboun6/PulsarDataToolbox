
.. module:: enterprise

.. note:: This tutorial was generated from a Jupyter notebook that can be
          downloaded `here <_static/notebooks/psrfits_write.ipynb>`_.

.. _psrfits_write:

Writing PSRFITS
===============

.. code:: python

    import numpy as np
    import pdat

Instantiate a draft file from a template
----------------------------------------

.. code:: python

    template = '../../../templates/search_template.fits'
    new_psrfits = 'my_psrfits.fits'

.. code:: python

    psrfits1=pdat.psrfits(new_psrfits,from_template=template)


.. parsed-literal::

    Making new SEARCH mode PSRFITS file using template from path:
    '../../../templates/search_template.fits'. 
    Writing to path 'my_psrfits.fits'.
    The Binary Table HDU headers will be written as they are added
    	 to the PSRFITS file.


The ``pdat`` package is very helpful for making PSRFITS file from
drafts. Many of the parameters in the ``PRIMARY`` and ``SUBINT`` HDUs
are codependent on one another, and the program keeps track of these
dependencies for the user. When you instantiate a ``psrfits`` with a
template a set of draft headers is made from the template so that you
can edit them before writing to disk. This “template-to-write” scheme
exists because many pieces of software that will analyze ``PSRFITS``
will baulk at files without a complete set of header information.

The template fits file is accessible as ``fits_template``.

.. code:: python

    def set_primary_header(psrfits_object,prim_dict):
        """
        prim_dict = dictionary of primary header changes
        """
        PF_obj = psrfits_object
        for key in prim_dict.keys():
            PF_obj.replace_FITS_Record('PRIMARY',key,prim_dict[key])
            
    def set_subint_header(psrfits_object,subint_dict):
        """
        prim_dict = dictionary of primary header changes
        """
        PF_obj = psrfits_object
        for key in subint_dict.keys():
            PF_obj.replace_FITS_Record('SUBINT',key,subint_dict[key])

.. code:: python

    def make_subint_BinTable(self):
        subint_draft = self.make_HDU_rec_array(self.nsubint, self.subint_dtype)
        return subint_draft

.. code:: python

    psrfits1.fits_template[0].read_header()['OBSERVER']




.. parsed-literal::

    'GALILEOGALILEI'



The draft headers are editable, and can be changed until you write the
file to disk. The ImageHDU that conatins the primary header is names
‘PRIMARY’. The others all go by the name of the ``EXTNAME``.
[‘PRIMARY’,‘SUBINT’,‘POLYCO’,‘HISTORY’,‘PARAM’]

.. code:: python

    psrfits1.draft_hdrs['SUBINT']




.. parsed-literal::

    
    XTENSION= 'BINTABLE'           / ***** Subintegration data  *****
    BITPIX  =                    8 / N/A
    NAXIS   =                    2 / 2-dimensional binary table
    NAXIS1  =             33636428 / width of table in bytes
    NAXIS2  =                    4 / Number of rows in table (NSUBINT)
    PCOUNT  =                    0 / size of special data area
    GCOUNT  =                    1 / one data group (required keyword)
    TFIELDS =                   17 / Number of fields per row
    TTYPE1  = 'TSUBINT '           / Length of subintegration
    TFORM1  = '1D      '           / Double
    TTYPE2  = 'OFFS_SUB'           / Offset from Start of subint centre
    TFORM2  = '1D      '           / Double
    TTYPE3  = 'LST_SUB '           / LST at subint centre
    TFORM3  = '1D      '           / Double
    TTYPE4  = 'RA_SUB  '           / RA (J2000) at subint centre
    TFORM4  = '1D      '           / Double
    TTYPE5  = 'DEC_SUB '           / Dec (J2000) at subint centre
    TFORM5  = '1D      '           / Double
    TTYPE6  = 'GLON_SUB'           / [deg] Gal longitude at subint centre
    TFORM6  = '1D      '           / Double
    TTYPE7  = 'GLAT_SUB'           / [deg] Gal latitude at subint centre
    TFORM7  = '1D      '           / Double
    TTYPE8  = 'FD_ANG  '           / [deg] Feed angle at subint centre
    TFORM8  = '1E      '           / Float
    TTYPE9  = 'POS_ANG '           / [deg] Position angle of feed at subint centre
    TFORM9  = '1E      '           / Float
    TTYPE10 = 'PAR_ANG '           / [deg] Parallactic angle at subint centre
    TFORM10 = '1E      '           / Float
    TTYPE11 = 'TEL_AZ  '           / [deg] Telescope azimuth at subint centre
    TFORM11 = '1E      '           / Float
    TTYPE12 = 'TEL_ZEN '           / [deg] Telescope zenith angle at subint centre
    TFORM12 = '1E      '           / Float
    TTYPE13 = 'DAT_FREQ'           / [MHz] Centre frequency for each channel
    TFORM13 = '2048E   '           / NCHAN floats
    TTYPE14 = 'DAT_WTS '           / Weights for each channel
    TFORM14 = '2048E   '           / NCHAN floats
    TTYPE15 = 'DAT_OFFS'           / Data offset for each channel
    TFORM15 = '8192E   '           / NCHAN*NPOL floats
    TTYPE16 = 'DAT_SCL '           / Data scale factor for each channel
    TFORM16 = '8192E   '           / NCHAN*NPOL floats
    TTYPE17 = 'DATA    '           / Subint data table
    TFORM17 = '33554432B'          / NBIN*NCHAN*NPOL*NSBLK int, byte(B) or bit(X)
    INT_TYPE= 'TIME    '           / Time axis (TIME, BINPHSPERI, BINLNGASC, etc)
    INT_UNIT= 'SEC     '           / Unit of time axis (SEC, PHS (0-1), DEG)
    SCALE   = 'FluxDen '           / Intensity units (FluxDen/RefFlux/Jansky)
    NPOL    =                    4 / Nr of polarisations
    POL_TYPE= 'IQUV    '           / Polarisation identifier (e.g., AABBCRCI, AA+BB)
    TBIN    = 0.000770559999999999 / [s] Time per bin or sample
    NBIN    =                    1 / Nr of bins (PSR/CAL mode; else 1)
    NBIN_PRD=                    0 / Nr of bins/pulse period (for gated data)
    PHS_OFFS=                   0. / Phase offset of bin 0 for gated data
    NBITS   =                    8 / Nr of bits/datum (SEARCH mode 'X' data, else 1)
    NSUBOFFS=                    0 / Subint offset (Contiguous SEARCH-mode files)
    NCHAN   =                 2048 / Number of channels/sub-bands in this file
    CHAN_BW =            -0.390625 / [MHz] Channel/sub-band width
    NCHNOFFS=                    0 / Channel/sub-band offset for split files
    NSBLK   =                 4096 / Samples/row (SEARCH mode, else 1)
    EXTNAME = 'SUBINT  '           / name of this binary table extension
    TUNIT1  = 's       '           / Units of field
    TUNIT2  = 's       '           / Units of field
    TUNIT3  = 's       '           / Units of field
    TUNIT4  = 'deg     '           / Units of field
    TUNIT5  = 'deg     '           / Units of field
    TUNIT6  = 'deg     '           / Units of field
    TUNIT7  = 'deg     '           / Units of field
    TUNIT8  = 'deg     '           / Units of field
    TUNIT9  = 'deg     '           / Units of field
    TUNIT10 = 'deg     '           / Units of field
    TUNIT11 = 'deg     '           / Units of field
    TUNIT12 = 'deg     '           / Units of field
    TUNIT13 = 'MHz     '           / Units of field
    TDIM17  = '(1,2048,4,4096)'    / Dimensions (NBITS or NBIN,NCHAN,NPOL,NSBLK)
    TUNIT17 = 'Jy      '           / Units of subint data
    EXTVER  =                    1 / auto assigned by template parser



In order to set the dimensions of the data arrays within the SUBINT HDU
there is a convenience function called ``set_subint_dims``. By setting
the dimensions using this function the dependencies on these dimensions,
inclduing memory allocation, will be propagated through the headers
correctly.

First lets choose some dimensions for the data.

.. code:: python

    sample_size = 20.48e-3 # in milliseconds
    ROWS = 30
    N_Time_Bins = 2048*ROWS 
    Total_time = round(N_Time_Bins*sample_size)
    dt = Total_time/N_Time_Bins
    subband =1.5625 
    BW=200
    N_freq = int(BW/subband)
    Npols = 4
    print('Total_time',Total_time/1e3)
    print('N_freq',N_freq)


.. parsed-literal::

    Total_time 1.258
    N_freq 128


And then call the ``set_subint_dims`` method.

.. code:: python

    psrfits1.set_subint_dims(nsblk=2048,nchan=N_freq,nsubint=ROWS,npol=Npols)

Once we have set the ``SUBINT`` dimensions a ``subint_dtype`` list is
made which we can then use to make a recarray to hold the data. Here
``nsubint`` is the same as above, and has been made an attribute.

.. code:: python

    subint_draft = psrfits1.make_HDU_rec_array(psrfits1.nsubint, psrfits1.subint_dtype)

All of the header cards can bet set by assigning them to the appropriate
member of the draft header.

.. code:: python

    npol = psrfits1.draft_hdrs['SUBINT']['NPOL']

Here we set the time per subintegration (time length of an NSBLK) and
the offsets, which are the times at the center of each subintegration
from the beginning of the observation.

.. code:: python

    tsubint = data.shape[-1]*dt*1e-3 #in seconds
    offs_sub_init = tsubint/2
    offs_sub = np.zeros((ROWS))
    
    for jj in range(ROWS):
        offs_sub[jj] = offs_sub_init + (jj * tsubint)

Here we just use the values from the template file.

.. code:: python

    lst_sub = psrfits1.fits_template[1]['LST_SUB'].read()[0]
    ra_sub = psrfits1.fits_template[1]['RA_SUB'].read()[0]
    dec_sub = psrfits1.fits_template[1]['DEC_SUB'].read()[0]
    glon_sub = psrfits1.fits_template[1]['GLON_SUB'].read()[0]
    glat_sub = psrfits1.fits_template[1]['GLAT_SUB'].read()[0]
    fd_ang = psrfits1.fits_template[1]['FD_ANG'].read()[0]
    pos_ang = psrfits1.fits_template[1]['POS_ANG'].read()[0]
    par_ang = psrfits1.fits_template[1]['PAR_ANG'].read()[0]
    tel_az = psrfits1.fits_template[1]['TEL_AZ'].read()[0]
    tel_zen = psrfits1.fits_template[1]['TEL_ZEN'].read()[0]
    
    ones = np.ones((ROWS))
    #And assign them using arrays of the appropriate sizes
    subint_draft['TSUBINT'] = tsubint * ones
    subint_draft['OFFS_SUB'] = offs_sub 
    subint_draft['LST_SUB'] = lst_sub * ones
    subint_draft['RA_SUB'] = ra_sub * ones
    subint_draft['DEC_SUB'] = dec_sub * ones
    subint_draft['GLON_SUB'] = glon_sub * ones
    subint_draft['GLAT_SUB'] = glat_sub * ones
    subint_draft['FD_ANG'] = fd_ang * ones
    subint_draft['POS_ANG'] = pos_ang * ones
    subint_draft['PAR_ANG'] = par_ang * ones
    subint_draft['TEL_AZ'] = tel_az * ones
    subint_draft['TEL_ZEN'] = tel_zen * ones

Here we’ll just make some data of the correct shape.

.. code:: python

    data = np.random.randn(ROWS,1,N_freq,Npols,2048)

And now we can assign the data arrays

.. code:: python

    for ii in range(subint_draft.size):
        subint_draft[ii]['DATA'] = data[ii,:,:,:,:]
        subint_draft[ii]['DAT_SCL'] = np.ones(N_freq*npol)
        subint_draft[ii]['DAT_OFFS'] = np.zeros(N_freq*npol)
        subint_draft[ii]['DAT_FREQ'] = np.linspace(1300,1500,N_freq)
        subint_draft[ii]['DAT_WTS'] = np.ones(N_freq)

.. code:: python

    subint_hdr=psrfits1.draft_hdrs['SUBINT']

.. code:: python

    from decimal import *
    getcontext().prec=12
    a=Decimal(S1.TimeBinSize*1e-3)
    a.to_eng_string()




.. parsed-literal::

    '0.00002047526041666666474943582498813299253015429712831974029541015625'



.. code:: python

    b='{0:1.18f}'.format(Decimal(a.to_eng_string()))
    b




.. parsed-literal::

    '0.000020475260416667'



.. code:: python

    pri_dic= {'OBSERVER':'GALILEOGALILEI','OBSFREQ':S1.f0,'OBSBW':S1.bw,'OBSNCHAN':S1.Nf}
    subint_dic = {'TBIN':b,'CHAN_BW':S1.freqBinSize}

.. code:: python

    subint_dic['TBIN']




.. parsed-literal::

    '0.000020475260416667'



.. code:: python

    psrfits1.make_FITS_card(subint_hdr,'TBIN',subint_dic['TBIN'])




.. parsed-literal::

    {'card_string': 'TBIN    = 0.000020475260416667 / [s] Time per bin or sample',
     'class': 150,
     'comment': '[s] Time per bin or sample',
     'dtype': 'F',
     'name': 'TBIN',
     'value': 2.0475260416667e-05,
     'value_orig': 2.0475260416667e-05}



.. code:: python

    psrfits1.draft_hdrs['SUBINT'].records()[65]




.. parsed-literal::

    {'card_string': "TUNIT8  = 'deg     '           / Units of field",
     'class': 70,
     'comment': 'Units of field',
     'dtype': 'C',
     'name': 'TUNIT8',
     'value': 'deg     ',
     'value_orig': 'deg     '}



.. code:: python

    set_primary_header(psrfits1,pri_dic)

.. code:: python

    set_subint_header(psrfits1,subint_dic)

.. code:: python

    psrfits1.draft_hdrs['SUBINT'].records()[47]['value'] = '0.000020483398437500'
    psrfits1.draft_hdrs['SUBINT'].records()[47]['value_orig'] = '0.000020483398437500'
    psrfits1.draft_hdrs['SUBINT'].records()[47]




.. parsed-literal::

    {'card_string': 'TBIN    = 0.000020475260416667 / [s] Time per bin or sample',
     'class': 150,
     'comment': '[s] Time per bin or sample',
     'dtype': 'F',
     'name': 'TBIN',
     'value': '0.000020483398437500',
     'value_orig': '0.000020483398437500'}



.. code:: python

    psrfits1.HDU_drafts['SUBINT'] = subint_draft

.. code:: python

    psrfits1.write_psrfits()

.. code:: python

    psrfits1.close()


.. parsed-literal::

    

