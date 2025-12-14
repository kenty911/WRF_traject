"""
Test script to verify netCDF4 library can be imported and used properly.
This test ensures that netCDF4 and its external dependencies work in the sandbox environment.
"""

import sys
import tempfile
import os


def test_netcdf4_import():
    """Test that netCDF4 can be imported."""
    try:
        import netCDF4
        print("✓ netCDF4 import successful")
        print(f"  netCDF4 version: {netCDF4.__version__}")
        return True
    except ImportError as e:
        print(f"✗ netCDF4 import failed: {e}")
        return False


def test_netcdf4_create_file():
    """Test that netCDF4 can create a file."""
    try:
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
            
            print("✓ netCDF4 file creation and reading successful")
            return True
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    except Exception as e:
        print(f"✗ netCDF4 file operations failed: {e}")
        return False


def test_all_dependencies():
    """Test that all required dependencies can be imported."""
    # Core dependencies that must work
    core_dependencies = {
        'numpy': 'numpy',
        'netCDF4': 'netCDF4',
        'pandas': 'pandas',
        'matplotlib': 'matplotlib',
    }
    
    # Dependencies that may fail due to compilation or compatibility issues
    optional_dependencies = {
        'wrf': 'wrf-python',  # Not included due to Python 3.12 incompatibility
        'geocat.f2py': 'geocat-f2py',  # May have Fortran compilation issues in some environments
    }
    
    required_success = True
    print("\nTesting core dependencies:")
    for module_name, package_name in core_dependencies.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name} import successful")
        except ImportError as e:
            print(f"✗ {package_name} import failed: {e}")
            required_success = False
    
    print("\nTesting optional dependencies:")
    for module_name, package_name in optional_dependencies.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name} import successful")
        except ImportError as e:
            print(f"⚠ {package_name} import failed (optional): {e}")
    
    return required_success


def main():
    """Run all tests."""
    print("=" * 60)
    print("netCDF4 and Dependencies Test")
    print("=" * 60)
    
    results = []
    
    # Test netCDF4 import
    results.append(("netCDF4 import", test_netcdf4_import()))
    
    # Test netCDF4 file operations
    results.append(("netCDF4 file operations", test_netcdf4_create_file()))
    
    # Test all dependencies
    results.append(("All dependencies", test_all_dependencies()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
