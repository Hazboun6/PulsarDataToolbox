
.. module:: enterprise

.. note:: This tutorial was generated from a Jupyter notebook that can be
          downloaded `here <_static/notebooks/pdat_intro.ipynb>`_.

.. _pdat_intro:

Pulsar Data Toolbox:
====================

``psrfits`` class
-----------------

The ``psrfits`` class allows easy access to the specialized FITS files
used in the Pulsar/Radio Astronomy community know as PSRFITS files. The
standard can be found on the `CSIRO Pulsar Group
website <http://www.atnf.csiro.au/people/pulsar/index.html?n=Main.Psrfits>`__.
In the current version of ``pdat`` this class is based on the Python
package ``fitsio`` which is a wrapper for the c-library ``cfitsio``. In
the future we plan to also make a version that uses the
``astropy.io.fits`` package, however the ``c`` library is fast,
efficient, allows appending and accessing of BinTables without loading
the whole file to memory. Since PSRFITS files carry large BinTables
these types of efficiencies are very useful.

Loading and Appending
---------------------

.. code:: python

    import pdat
    import os

.. code:: python

    pFits1 = '../../../templates/search_scratch.fits'
    pFits2 = '../../../templates/search_template.fits'

Check file sizes
----------------

.. code:: python

    a=os.path.getsize(pFits1)
    b=os.path.getsize(pFits2)
    print('Size of 1st file:',a)
    print('Size of 2nd file:',b)


.. parsed-literal::

    Size of 1st file: 5302080
    Size of 2nd file: 5302080


Load files
----------

.. code:: python

    psrf1 = pdat.psrfits(pFits1)


.. parsed-literal::

    Loading PSRFITS file from path:
    '../../../templates/search_scratch.fits'.


Append the Secondary BinTables to an existing PSRFITS
-----------------------------------------------------

The ``append_from_file`` method appends all of the secondary BinTables
of a PSRFITS, given as a file path, to the already loaded PSRFITS. The
secondary BinTables include ``SUBINT``,\ ``POLYCO``, ``HISTORY`` and
``PARAM``. This is only possible between identical ``mode`` files
(``SEARCH``, ``PSR`` or ``CAL``). By default the order of the tables is
assumed identical. If the BinTables are in different orders there is an
optional ``table`` flag to provide a list of the order of the original
BinTables. Alternatively, you may only select a subset of BinTables to
append.

.. code:: python

    psrf1.append_from_file(pFits2)

.. code:: python

    os.path.getsize(pFits1)




.. parsed-literal::

    5302080



Checking the size we see it has grown, but not doubled. That is because
the ``PRIMARY`` header was not changed.

The ``psrfits`` class comes with all of the functionality built into
``fitsio``. The class represents a list of HDUs. The header information
is accesible through the ``read_header`` method.

.. code:: python

    psrf1[1].read_header()




.. parsed-literal::

    
    XTENSION= 'BINTABLE'           / ***** Subintegration data  *****
    BITPIX  =                    8 / N/A
    NAXIS   =                    2 / 2-dimensional binary table
    NAXIS1  =               264268 / width of table in bytes
    NAXIS2  =                   20 / Number of rows in table (NSUBINT)
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
    TFORM13 = '    128E'           / NCHAN floats
    TTYPE14 = 'DAT_WTS '           / Weights for each channel
    TFORM14 = '    128E'           / NCHAN floats
    TTYPE15 = 'DAT_OFFS'           / Data offset for each channel
    TFORM15 = '    128E'           / NCHAN*NPOL floats
    TTYPE16 = 'DAT_SCL '           / Data scale factor for each channel
    TFORM16 = '    128E'           / NCHAN*NPOL floats
    TTYPE17 = 'DATA    '           / Subint data table
    TFORM17 = '  262144B'          / NBIN*NCHAN*NPOL*NSBLK int, byte(B) or bit(X)
    TDIM17  = '(1, 128, 1, 2048)'  / Dimensions (NBITS or NBIN,NCHAN,NPOL,NSBLK)
    INT_TYPE= 'TIME    '           / Time axis (TIME, BINPHSPERI, BINLNGASC, etc)
    INT_UNIT= 'SEC     '           / Unit of time axis (SEC, PHS (0-1), DEG)
    SCALE   = 'FluxDen '           / Intensity units (FluxDen/RefFlux/Jansky)
    NPOL    =                    1 / Nr of polarisations
    POL_TYPE= 'IQUV    '           / Polarisation identifier (e.g., AABBCRCI, AA+BB)
    TBIN    =    2.04833984375E-05 / [s] Time per bin or sample
    NBIN    =                    1 / Nr of bins (PSR/CAL mode; else 1)
    NBIN_PRD=                    0 / Nr of bins/pulse period (for gated data)
    PHS_OFFS=                   0. / Phase offset of bin 0 for gated data
    NBITS   =                    8 / Nr of bits/datum (SEARCH mode 'X' data, else 1)
    NSUBOFFS=                    0 / Subint offset (Contiguous SEARCH-mode files)
    NCHAN   =                  128 / Number of channels/sub-bands in this file
    CHAN_BW =               1.5625 / [MHz] Channel/sub-band width
    NCHNOFFS=                    0 / Channel/sub-band offset for split files
    NSBLK   =                 2048 / Samples/row (SEARCH mode, else 1)
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
    TUNIT17 = 'Jy      '           / Units of subint data
    EXTVER  =                    1 / auto assigned by template parser



The data in a ``PSRFITS`` is found in the ``SUBINT`` BinTable.

.. code:: python

    psrf1




.. parsed-literal::

    
      file: ../../../templates/search_scratch.fits
      mode: READWRITE
      extnum hdutype         hduname[v]
      0      IMAGE_HDU       
      1      BINARY_TBL      SUBINT[1]



Here ``SUBINT`` is the 2nd HDU. The data is accesible as a
``numpy.recarray`` with ``NSUBINT`` rows. Think of a recarray as a
spreadsheet where the individual entries can be strings, floats or whole
arrays.

.. code:: python

    data=psrf1[1].read()
    print(data.shape)
    data.dtype.descr


.. parsed-literal::

    (20,)




.. parsed-literal::

    [('TSUBINT', '>f8'),
     ('OFFS_SUB', '>f8'),
     ('LST_SUB', '>f8'),
     ('RA_SUB', '>f8'),
     ('DEC_SUB', '>f8'),
     ('GLON_SUB', '>f8'),
     ('GLAT_SUB', '>f8'),
     ('FD_ANG', '>f4'),
     ('POS_ANG', '>f4'),
     ('PAR_ANG', '>f4'),
     ('TEL_AZ', '>f4'),
     ('TEL_ZEN', '>f4'),
     ('DAT_FREQ', '>f4', (128,)),
     ('DAT_WTS', '>f4', (128,)),
     ('DAT_OFFS', '>f4', (128,)),
     ('DAT_SCL', '>f4', (128,)),
     ('DATA', '|u1', (2048, 1, 128, 1))]



While the ``DATA`` array above is 4 dimensional (this is the case in
``SEARCH`` files, it is 3 dimensional in ``PSR`` and ``CAL`` files).
However there are ``NSUBINT`` of those arrays. To access the data one
uses the name of the column, ``DATA``, then a single entry square
bracket denoting the row. This gives one of the ``NSUBINT`` arrays in
the BinTable.

.. code:: python

    data['DATA'][0].shape




.. parsed-literal::

    (2048, 1, 128, 1)



This object is then a normal numpy array that can be accessed with numpy
array slice notation. Access a single entry by choosing four integers in
the range of dimensions.

.. code:: python

    data['DATA'][0][1000,0,3,0]




.. parsed-literal::

    7



Other arrays are accessed similarly, but without as many indices. There
are ``NSUBINT`` rows of 1-dimensional arrays for each of the ``DAT_X``
parameters and ``NSUBINT`` floats of the other entries.

.. code:: python

    print(data['DAT_OFFS'].shape)
    data['DAT_OFFS'][2]


.. parsed-literal::

    (20, 128)




.. parsed-literal::

    array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.], dtype=float32)



.. code:: python

    print(data['GLON_SUB'].shape)
    data['GLON_SUB'][2]


.. parsed-literal::

    (20,)




.. parsed-literal::

    97.721010667684681



One can clear the file from memory using the ``close`` method.

.. code:: python

    psrf1.close()


.. parsed-literal::

    


``PSR`` and ``CAL`` files
-------------------------

The PSRFITS standard actually has many BinTable extensions, and many
files come with more than two HDUs. The ``psrfits`` class will
generically build a Python version of any of these file types. In this
package there are three template types, corresponding to the three most
common file types used by the NANOGrav Pulsar Timing array. If you would
like another template included please start an issue on our GitHub page.

A ``PSR`` mode file is data from an observation where the data is folded
at the frequency of the pulsar to build up signal-to-noise ratio in real
time. A ``CAL`` file has the same set of HDUs but is not folded. It is
data take of a calibration source. Here we access the ``PSR`` template
file and look at a different BinTable extension.

.. code:: python

    pFits3 = '../../../templates/psr_template.fits'
    psrf2 = pdat.psrfits(pFits3)


.. parsed-literal::

    Loading PSRFITS file from path:
    '/Users/jeffrey/PSS/guppi_57691_J1909-3744_0004_0001.fits'.


.. code:: python

    psrf2




.. parsed-literal::

    
      file: /Users/jeffrey/PSS/guppi_57691_J1909-3744_0004_0001.fits
      mode: READWRITE
      extnum hdutype         hduname[v]
      0      IMAGE_HDU       
      1      BINARY_TBL      HISTORY[1]
      2      BINARY_TBL      PSRPARAM[1]
      3      BINARY_TBL      POLYCO[1]
      4      BINARY_TBL      SUBINT[1]



.. code:: python

    psrf2[3].read_header()




.. parsed-literal::

    
    XTENSION= 'BINTABLE'           / ***** Polyco history *****
    BITPIX  =                    8 / N/A
    NAXIS   =                    2 / 2-dimensional binary table
    NAXIS1  =                  222 / width of table in bytes
    NAXIS2  =                    1 / number of rows in table
    PCOUNT  =                    0 / size of special data area
    GCOUNT  =                    1 / one data group (required keyword)
    TFIELDS =                   13 / Number of fields per row
    TTYPE1  = 'DATE_PRO'           / Polyco creation date and time (UTC)
    TFORM1  = '24A     '           / 24-char string
    TTYPE2  = 'POLYVER '           / Polyco version ID
    TFORM2  = '16A     '           / 16-char string
    TTYPE3  = 'NSPAN   '           / Span of polyco block in min
    TFORM3  = '1I      '           / Integer
    TTYPE4  = 'NCOEF   '           / Nr of coefficients (<=15)
    TFORM4  = '1I      '           / Integer
    TTYPE5  = 'NPBLK   '           / Nr of blocks (rows) for this polyco
    TFORM5  = '1I      '           / Integer
    TTYPE6  = 'NSITE   '           / Observatory code
    TFORM6  = '8A      '           / 8-char string
    TTYPE7  = 'REF_FREQ'           / Reference frequency for phase
    TFORM7  = '1D      '           / Double
    TTYPE8  = 'PRED_PHS'           / Predicted pulse phase at observation start
    TFORM8  = '1D      '           / Double
    TTYPE9  = 'REF_MJD '           / Reference MJD
    TFORM9  = '1D      '           / Double
    TTYPE10 = 'REF_PHS '           / Reference phase
    TFORM10 = '1D      '           / Double
    TTYPE11 = 'REF_F0  '           / Zero-order pulsar frequency
    TFORM11 = '1D      '           / Double
    TTYPE12 = 'LGFITERR'           / Log_10 of polynomial fit rms error in periods
    TFORM12 = '1D      '           / Double
    TTYPE13 = 'COEFF   '           / Polyco coefficients
    TFORM13 = '15D     '           / NCOEF doubles
    EXTNAME = 'POLYCO  '           / name of this binary table extension
    TUNIT7  = 'MHz     '           / Units of field
    TUNIT11 = 'Hz      '           / Units of field
    EXTVER  =                    1 / auto assigned by template parser



.. code:: python

    psrf2[3]['COEFF'][:]




.. parsed-literal::

    array([[  6.37061369e-07,  -3.84007940e-01,   1.63071384e-03,
             -1.91944367e-06,   1.07255013e-09,   6.72218368e-12,
             -8.60574070e-12,   1.25507648e-13,   1.71341258e-14,
             -2.97308173e-16,  -1.79229301e-17,   2.50414099e-19,
              9.50130849e-21,  -7.26854989e-23,  -2.02121757e-24]])



.. code:: python

    psrf2[2]['PARAM'][:]




.. parsed-literal::

    array([ b'PSRJ              1909-3744                                                                                                     ',
           b'RAJ               19:09:47.4380095699897                                                                                        ',
           b'DECJ             -37:44:14.3162347000103                                                                                        ',
           b'PEPOCH            53000.0000000000000000                                                                                        ',
           b'F                 3.3931569275871846D+02                                                                                        ',
           b'F1               -1.6150815823660001D+00                                                                                        ',
           b'PMDEC            -3.6776299999999999D+01                                                                                        ',
           b'PMRA             -9.5500000000000007D+00                                                                                        ',
           b'POSEPOCH          53000.0000000000000000                                                                                        ',
           b'PX                1.3517999999999999D+00                                                                                        ',
           b'DM                1.0394679999999999D+01                                                                                        ',
           b'START             53219.2149999999965075                                                                                        ',
           b'FINISH            54614.2710000000006403                                                                                        ',
           b'CLK               UTC(NIST)                                                                                                     ',
           b'EPHEM             DE405                                                                                                         ',
           b'TZRMJD            53293.02028990324198077                                                                                       ',
           b'TZRFRQ            8.4256500000000005D+02                                                                                        ',
           b'TZRSITE           1                                                                                                             ',
           b'BINARY            ELL1                                                                                                          ',
           b'A1                1.8979909859999999D+00                                                                                        ',
           b'PB                1.5334494510779999D+00                                                                                        ',
           b'SINI              9.9727800000000000D-01                                                                                        ',
           b'M2                2.2327900000000001D-01                                                                                        ',
           b'EPS1              3.7300000000000003D-08                                                                                        ',
           b'EPS2              1.1340000000000000D-07                                                                                        ',
           b'TASC              53113.9505872139998246                                                                                        ',
           b'TRES              4.2999999999999999D-01                                                                                        ',
           b'NTOA              746                                                                                                           '],
          dtype='|S128')



Glossary:
---------

**BinTable**: A table of binary data.

**HDU**: Header Unit. The main division of a FITS file.

**ImageHDU**: An HDU that either holds a 2-d data array, usually
represnting an image, of the primary HDU, acting as the main header file
for the FITS file.

**SUBINT HDU**: The BinTable extension (HDU) that holds the data from a
pulsar/radio observation. In a ``PSR`` (folded) mode PSRFITS file these
are actually subintegrations of folded pulsar data.

**HISTORY HDU**: The BinTable extension (HDU) that has some information
about the history of the observation and what may have been done to the
data in the file.

**FITS Card**: The header information in FITS files is held in a FITS
card. In Python these are usually held as dictionary-type variables.
There is a ``card string`` which hold the information that appears when
you call the header. One of the dictionary entries is the actual value
called when accesing the data.

**POLYCO HDU**: The BinTable extension (HDU) that has a list of the
Chebyshev polynomial coefficients used for a short timescale timing
model when using the backend of a telescope in ‘PSR’ (folding) mode.

**PARAM HDU**: The BinTable extensino (HDU) that hols the parameters of
the pulsar. Most often these are text lines taken from a ``.par``
(parameter) file.
