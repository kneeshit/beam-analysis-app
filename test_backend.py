#!/usr/bin/env python3
"""
Test script to verify backend is working
"""
import requests
import json
import time

def test_backend():
    base_url = "http://127.0.0.1:8000"
    
    print("Testing Backend Connection...")
    print("=" * 40)
    
    # Test 1: Basic connection
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✓ Backend is running and responding")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend. Make sure it's running on port 8000")
        return False
    except Exception as e:
        print(f"✗ Error connecting to backend: {e}")
        return False
    
    # Test 2: Create session
    try:
        response = requests.post(f"{base_url}/api/session/create", timeout=5)
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data['session_id']
            print(f"✓ Session created successfully: {session_id}")
        else:
            print(f"✗ Failed to create session: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error creating session: {e}")
        return False
    
    # Test 3: Set beam properties
    try:
        beam_props = {
            "length": 10.0,
            "support1": 2.0,
            "support2": 8.0,
            "modulus_of_elasticity": 200e9,
            "second_moment_of_area": 1e-4
        }
        response = requests.post(
            f"{base_url}/api/session/{session_id}/beam-properties",
            json=beam_props,
            timeout=5
        )
        if response.status_code == 200:
            print("✓ Beam properties set successfully")
        else:
            print(f"✗ Failed to set beam properties: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error setting beam properties: {e}")
        return False
    
    # Test 4: Add a load
    try:
        load_data = {
            "load_type": "Point Force",
            "load_data": {
                "magnitude": 1000,
                "location": 5.0
            }
        }
        response = requests.post(
            f"{base_url}/api/session/{session_id}/loads/add",
            json=load_data,
            timeout=5
        )
        if response.status_code == 200:
            print("✓ Load added successfully")
        else:
            print(f"✗ Failed to add load: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error adding load: {e}")
        return False
    
    # Test 5: Calculate analysis
    try:
        response = requests.post(
            f"{base_url}/api/session/{session_id}/calculate",
            timeout=10
        )
        if response.status_code == 200:
            results = response.json()
            print("✓ Analysis calculation successful")
            print(f"  Max shear force: {results['max_shear_force']:.2f} N")
            print(f"  Max bending moment: {results['max_bending_moment']:.2f} N⋅m")
        else:
            print(f"✗ Failed to calculate analysis: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error calculating analysis: {e}")
        return False
    
    print("\n✓ All backend tests passed!")
    print("Backend is working correctly.")
    return True

if __name__ == "__main__":
    print("Backend Test Script")
    print("Make sure the backend server is running first!")
    print("Run: cd backend && python start_server.py")
    print()
    
    # Wait a moment for user to read
    time.sleep(2)
    
    success = test_backend()
    
    if success:
        print("\n" + "=" * 40)
        print("Backend is ready for frontend connection!")
        print("You can now start the frontend with: cd frontend && npm start")
    else:
        print("\n" + "=" * 40)
        print("Backend test failed. Check the error messages above.")
        print("Make sure:")
        print("1. Backend dependencies are installed: pip install -r backend/requirements.txt")
        print("2. Backend server is running: cd backend && python start_server.py")
        print("3. No firewall is blocking port 8000")
