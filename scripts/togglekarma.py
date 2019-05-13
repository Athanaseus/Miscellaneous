#! /usr/bin/env python
# Script to convert a data cube as produced by MeerKATHI to Karma-understandable format

# Usage: convertokarma.py bla.fits

from astropy.io import fits
import sys

def toggleheader(thefitsfile):
    """
    Convert header of data cube as produced by MeerKATHI to karma-readable or back

    Input:
    thefitsfile(str): Input fits file
    
    Convert header velocity units to something that Karma will
    understand if MeerKATHI format is found, convert back if
    Karma-readable is found.

    """
    hdulist = fits.open(thefitsfile, mode='update')

    header = hdulist[0].header

    if 'VRAD' in header['ctype3']:
        print('Converting to Karma-readable')
        header['ctype3'] = 'VELO-HEL'
        header['cdelt3'] = header['cdelt3']/1000.
        header['crval3'] = header['crval3']/1000.
    else:
        if header['ctype3'] == 'VELO-HEL':
            print('Converting to WCS-compliant')
            header['ctype3'] = 'VRAD'
            header['cdelt3'] = header['cdelt3']*1000.
            header['crval3'] = header['crval3']*1000.
        else:
            print('It does not look as if the file was generated by MeerKATHI, doing nothing.')

    hdulist.flush()
    hdulist.close()

    
if __name__ == "__main__":
    try:
        toggleheader(sys.argv[1])
    except:
        print('Usage: togglekarma.py bla.fits')
        sys.exit()
