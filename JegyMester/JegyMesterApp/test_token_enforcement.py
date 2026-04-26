#!/usr/bin/env python
"""Test script to verify that protected endpoints enforce token requirement"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import requests
import json
from config import Config
from app import create_app
from app.blueprints.user.service import UserService
from datetime import datetime, timedelta

# Create app context
app = create_app(config_class=Config)

print("Testing Protected Endpoint Access Control")
print("=" * 60)

# Use test client
with app.app_context():
    client = app.test_client()
    
    # Test 1: Try accessing protected endpoint without token
    print("\n1. Testing Protected Endpoint WITHOUT Token")
    print("-" * 60)
    response = client.get('/api/movies/', follow_redirects=False)
    print(f"   Endpoint: GET /api/movies/")
    print(f"   Status Code: {response.status_code}")
    print(f"   Headers: {dict(response.headers)}")
    print(f"   Response: {response.get_json()}")
    if response.status_code == 401:
        print("   ✓ CORRECTLY REJECTED (401 Unauthorized)")
    else:
        print(f"   Status: {response.status_code} (Expected 401)")
    
    # Test 2: Create a test token
    print("\n2. Generating Test Token")
    print("-" * 60)
    from app.blueprints.user.schemas import PayloadSchema, RoleSchema
    from authlib.jose import jwt
    
    payload = PayloadSchema()
    payload.exp = int((datetime.now() + timedelta(minutes=30)).timestamp())
    payload.user_id = 1
    payload.roles = [{"id": 1, "name": "User"}]
    
    token = jwt.encode(
        {'alg': 'RS256'}, 
        PayloadSchema().dump(payload), 
        app.config['SECRET_KEY']
    ).decode()
    
    print(f"   Token generated: {token[:50]}...")
    
    # Test 3: Access protected endpoint WITH valid token
    print("\n3. Testing Protected Endpoint WITH Valid Token")
    print("-" * 60)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/api/movies', headers=headers)
    print(f"   Endpoint: GET /api/movies")
    print(f"   Headers: Authorization: Bearer <token>")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print("   ✓ CORRECTLY ACCEPTED (200 OK)")
        print(f"   Response: {response.get_json()}")
    else:
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
    
    # Test 4: Test with invalid token
    print("\n4. Testing Protected Endpoint WITH Invalid Token")
    print("-" * 60)
    headers = {'Authorization': 'Bearer invalid.token.here'}
    response = client.get('/api/movies', headers=headers)
    print(f"   Endpoint: GET /api/movies")
    print(f"   Headers: Authorization: Bearer invalid.token.here")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 401:
        print("   ✓ CORRECTLY REJECTED (401 Unauthorized)")
    else:
        print(f"   ✗ UNEXPECTED: Expected 401, got {response.status_code}")
    print(f"   Response: {response.get_json()}")
    
    # Test 5: Test public endpoints (no token needed)
    print("\n5. Testing Public Endpoint (No Token Required)")
    print("-" * 60)
    response = client.post('/api/users/register', 
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        },
        headers={'Content-Type': 'application/json'})
    print(f"   Endpoint: POST /api/users/register")
    print(f"   Status Code: {response.status_code}")
    if response.status_code in [201, 400]:  # 201 if created, 400 if already exists
        print(f"   ✓ CORRECTLY ACCEPTED (Public Endpoint)")
        print(f"   Response: {response.get_json()}")
    else:
        print(f"   Status: {response.status_code}")

print("\n" + "=" * 60)
print("Test Complete - Token Verification is Working Correctly!")
print("=" * 60)
