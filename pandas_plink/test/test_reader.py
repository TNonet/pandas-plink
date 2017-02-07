from __future__ import unicode_literals

from os.path import dirname, join, realpath

from numpy import array
from numpy.testing import assert_array_equal

from pandas_plink import read_plink

def _ascii_airlock(v):
    if not isinstance(v, bytes):
        v = v.encode()
    return v

def test_read_plink():
    datafiles = join(dirname(realpath(__file__)), 'data_files')
    file_prefix = join(datafiles, 'data')

    (bim, fam, bed) = read_plink(file_prefix)

    assert_array_equal(bim.loc[('1', 72515), 'snp'], ['rs4030300'])
    assert_array_equal(bim.loc[('1', ), :].shape, [10, 5])
    assert_array_equal(fam.loc[('Sample_2', 'Sample_2'), 'trait'], ['-9'])



def test_read_bed_block():
    from pandas_plink._bed_read import read_bed_chunk

    datafiles = join(dirname(realpath(__file__)), 'data_files')
    file_prefix = join(datafiles, 'data')

    row_start = 0
    row_end = 10
    col_start = 0
    col_end = 3

    bed = read_bed_chunk(_ascii_airlock(file_prefix + '.bed'), 10, 3,
                         row_start, row_end, col_start,
                         col_end)

    assert_array_equal(bed,
                       array([[2, 2, 1], [2, 1, 2], [3, 3, 3], [3, 3, 1],
                              [2, 2, 2], [2, 2, 2], [2, 1, 0], [2, 2, 2],
                              [1, 2, 2], [2, 1, 2]]))

    bed = read_bed_chunk(_ascii_airlock(file_prefix + '.bed'), 10, 3,
                         1, 2, 1, 3)

    assert_array_equal(bed, [1, 2])
