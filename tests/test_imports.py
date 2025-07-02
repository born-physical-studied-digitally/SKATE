"""
Test that the reorganized package can be imported correctly.
"""

import sys
import os

# Add the src directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_package_import():
    """Test that the main package can be imported."""
    import seismogram_pipeline
    assert seismogram_pipeline.__version__ == "1.0.0"

def test_core_modules_import():
    """Test that core modules can be imported."""
    from seismogram_pipeline.core import roi_detection, meanline_detection, intersection_detection
    assert roi_detection is not None
    assert meanline_detection is not None
    assert intersection_detection is not None

def test_cli_modules_import():
    """Test that CLI modules can be imported."""
    from seismogram_pipeline.cli import get_roi, get_meanlines, get_all_metadata
    assert get_roi is not None
    assert get_meanlines is not None
    assert get_all_metadata is not None

def test_main_functions_import():
    """Test that main functions can be imported."""
    from seismogram_pipeline import get_roi, detect_meanlines, find_intersections
    assert get_roi is not None
    assert detect_meanlines is not None
    assert find_intersections is not None

if __name__ == "__main__":
    # Run tests
    test_package_import()
    test_core_modules_import()
    test_cli_modules_import()
    test_main_functions_import()
    print("All import tests passed!") 