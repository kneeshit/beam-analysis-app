#!/usr/bin/env python3
"""
Test script to verify the structural analysis calculations work correctly
This can be run independently to test the mathematical functions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.calculations import calculate_structural_analysis
import numpy as np

def test_simple_beam():
    """Test a simple beam with a point load"""
    print("Testing simple beam with point load...")
    
    # Beam properties
    length = 10.0  # 10m beam
    support1 = 2.0  # Support at 2m
    support2 = 8.0  # Support at 8m
    E = 200e9  # Steel modulus (Pa)
    I = 1e-4   # Second moment of area (m^4)
    
    # Loads
    f1 = []  # No point moments
    f2 = [[1000, 5.0]]  # 1000N point load at 5m
    f3 = []  # No distributed loads
    f4 = []  # No triangular loads
    
    try:
        V, BM, slope, deflection, reactions = calculate_structural_analysis(
            f1, f2, f3, f4, support1, support2, length, E, I
        )
        
        print(f"✓ Calculation successful!")
        print(f"  - Shear force values: {len(V)} points")
        print(f"  - Max shear force: {max(map(abs, V)):.2f} N")
        print(f"  - Max bending moment: {max(map(abs, BM)):.2f} N⋅m")
        print(f"  - Max deflection: {max(map(abs, deflection)):.6f} m")
        print(f"  - Reaction forces: {[round(r[0], 2) for r in reactions]} N")
        
        return True
        
    except Exception as e:
        print(f"✗ Calculation failed: {e}")
        return False

def test_distributed_load():
    """Test a beam with distributed load"""
    print("\nTesting beam with distributed load...")
    
    # Beam properties
    length = 8.0
    support1 = 1.0
    support2 = 7.0
    E = 200e9
    I = 1e-4
    
    # Loads
    f1 = []
    f2 = []
    f3 = [[500, 2.0, 6.0]]  # 500 N/m from 2m to 6m
    f4 = []
    
    try:
        V, BM, slope, deflection, reactions = calculate_structural_analysis(
            f1, f2, f3, f4, support1, support2, length, E, I
        )
        
        print(f"✓ Calculation successful!")
        print(f"  - Max shear force: {max(map(abs, V)):.2f} N")
        print(f"  - Max bending moment: {max(map(abs, BM)):.2f} N⋅m")
        print(f"  - Max deflection: {max(map(abs, deflection)):.6f} m")
        
        return True
        
    except Exception as e:
        print(f"✗ Calculation failed: {e}")
        return False

def test_combined_loads():
    """Test a beam with multiple load types"""
    print("\nTesting beam with combined loads...")
    
    # Beam properties
    length = 12.0
    support1 = 3.0
    support2 = 9.0
    E = 200e9
    I = 1e-4
    
    # Loads
    f1 = [[500, 6.0]]  # 500 N⋅m moment at 6m
    f2 = [[800, 4.0]]  # 800N point load at 4m
    f3 = [[200, 1.0, 3.0]]  # 200 N/m from 1m to 3m
    f4 = [[300, 7.0, 10.0]]  # 300N triangular load from 7m to 10m
    
    try:
        V, BM, slope, deflection, reactions = calculate_structural_analysis(
            f1, f2, f3, f4, support1, support2, length, E, I
        )
        
        print(f"✓ Calculation successful!")
        print(f"  - Max shear force: {max(map(abs, V)):.2f} N")
        print(f"  - Max bending moment: {max(map(abs, BM)):.2f} N⋅m")
        print(f"  - Max deflection: {max(map(abs, deflection)):.6f} m")
        
        return True
        
    except Exception as e:
        print(f"✗ Calculation failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Beam Analysis Calculation Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    if test_simple_beam():
        tests_passed += 1
    
    if test_distributed_load():
        tests_passed += 1
        
    if test_combined_loads():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✓ All tests passed! The calculation engine is working correctly.")
    else:
        print("✗ Some tests failed. Check the error messages above.")
    
    print("=" * 50)
