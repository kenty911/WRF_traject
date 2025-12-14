"""
Test script to verify netCDF4 library can be imported and used properly.
This test ensures that netCDF4 and its external dependencies work in the sandbox environment.

Run with pytest:
    pytest test_netcdf4.py -v
"""

import tempfile
import os
import pytest


def test_netcdf4_import():
    """Test that netCDF4 can be imported."""
    import netCDF4
    assert netCDF4.__version__ is not None


def test_netcdf4_create_file():
    """Test that netCDF4 can create a file."""
    from netCDF4 import Dataset
    import numpy as np

    # Create a temporary file that gets deleted automatically
    fd, tmp_path = tempfile.mkstemp(suffix='.nc')
    os.close(fd)

    try:
        # Create a netCDF file
        with Dataset(tmp_path, 'w', format='NETCDF4') as nc:
            # Create a dimension
            nc.createDimension('x', 10)
            nc.createDimension('y', 10)

            # Create a variable
            var = nc.createVariable('data', 'f4', ('x', 'y'))
            var[:] = np.random.rand(10, 10)

        # Read the file back
        with Dataset(tmp_path, 'r') as nc:
            data = nc.variables['data'][:]
            assert data.shape == (10, 10), f"Expected shape (10, 10), got {data.shape}"

    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_numpy_import():
    """Test that numpy can be imported."""
    import numpy as np
    assert np.__version__ is not None


def test_pandas_import():
    """Test that pandas can be imported."""
    import pandas as pd
    assert pd.__version__ is not None


def test_matplotlib_import():
    """Test that matplotlib can be imported."""
    import matplotlib
    assert matplotlib.__version__ is not None


def test_wrf_python_import():
    """Test that wrf-python can be imported (optional)."""
    pytest.importorskip("wrf", reason="wrf-python not installed (optional)")


def test_geocat_f2py_import():
    """Test that geocat-f2py can be imported (optional)."""
    pytest.importorskip("geocat.f2py", reason="geocat-f2py may have compilation issues (optional)")
