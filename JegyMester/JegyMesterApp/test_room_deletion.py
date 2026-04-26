#!/usr/bin/env python
"""Test script to verify room deletion constraint check"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import Config
from app import create_app
from app.blueprints.rooms.service import RoomService
from app.blueprints.seat.service import SeatService
from app.blueprints.screenings.service import ScreeningService
from app.blueprints.movies.service import MovieService

print("Testing Room Deletion Constraint Check")
print("=" * 60)

# Create app context
app = create_app(config_class=Config)

with app.app_context():
    # Test 1: Create a test room
    print("\n1. Creating Test Room")
    print("-" * 60)
    import time
    room_name = f"TestRoom_{int(time.time())}"
    room_data = {
        "name": room_name,
        "total_capacity": 100
    }
    success, response = RoomService.create_room(room_data)
    if success:
        room_data = response
        room_id = room_data["id"]
        print(f"   [OK] Created room: {room_data}")
    else:
        print(f"   [FAIL] Failed to create room: {response}")
        sys.exit(1)

    # Test 2: Create seats for the room
    print("\n2. Creating Seats for the Room")
    print("-" * 60)
    seat_data = {
        "room_id": room_id,
        "row_num": 1,
        "seat_num": 1
    }
    success, response = SeatService.create_seat(seat_data)
    if success:
        seat_id = response["id"]
        print(f"   [OK] Created seat: {response}")
    else:
        print(f"   [FAIL] Failed to create seat: {response}")
        sys.exit(1)

    # Test 3: Try to delete room while it has seats (should fail)
    print("\n3. Attempting to Delete Room with Seats Assigned")
    print("-" * 60)
    success, response = RoomService.delete_room(room_id)
    if not success:
        print(f"   [OK] Correctly prevented deletion: {response}")
    else:
        print(f"   [FAIL] Should not have allowed deletion: {response}")
        sys.exit(1)

    # Test 4: Create a movie for screening
    print("\n4. Creating Test Movie for Screening")
    print("-" * 60)
    movie_data = {
        "title": f"TestMovie_{int(time.time())}",
        "description": "Test movie for screening",
        "duration_minutes": 120
    }
    success, response = MovieService.create_movie(movie_data)
    if success:
        movie_id = response["id"]
        print(f"   [OK] Created movie: {response}")
    else:
        print(f"   [FAIL] Failed to create movie: {response}")
        sys.exit(1)

    # Test 5: Create a screening for the room
    print("\n5. Creating Screening for the Room")
    print("-" * 60)
    from datetime import datetime, timedelta
    screening_data = {
        "movie_id": movie_id,
        "room_id": room_id,
        "start_time": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
    }
    success, response = ScreeningService.create_screening(screening_data)
    if success:
        screening_id = response["id"]
        print(f"   [OK] Created screening: {response}")
    else:
        print(f"   [FAIL] Failed to create screening: {response}")
        sys.exit(1)

    # Test 6: Try to delete room while it has screenings (should fail)
    print("\n6. Attempting to Delete Room with Screenings Scheduled")
    print("-" * 60)
    success, response = RoomService.delete_room(room_id)
    if not success:
        print(f"   [OK] Correctly prevented deletion: {response}")
    else:
        print(f"   [FAIL] Should not have allowed deletion: {response}")
        sys.exit(1)

    # Test 7: Remove screening and seats from room
    print("\n7. Removing Screening and Seats from Room")
    print("-" * 60)
    # Delete screening
    success1, response1 = ScreeningService.delete_screening(screening_id)
    # Delete seat
    success2, response2 = SeatService.delete_seat(seat_id)

    if success1 and success2:
        print(f"   [OK] Removed screening and seat from room")
    else:
        print(f"   [FAIL] Failed to remove: screening={response1}, seat={response2}")
        sys.exit(1)

    # Test 8: Try to delete room again (should succeed now)
    print("\n8. Attempting to Delete Room After Removing Dependencies")
    print("-" * 60)
    success, response = RoomService.delete_room(room_id)
    if success:
        print(f"   [OK] Successfully deleted room: {response}")
    else:
        print(f"   [FAIL] Should have allowed deletion: {response}")

    # Test 9: Try to delete non-existent room
    print("\n9. Attempting to Delete Non-existent Room")
    print("-" * 60)
    success, response = RoomService.delete_room(99999)
    if not success:
        print(f"   [OK] Correctly handled non-existent room: {response}")
    else:
        print(f"   [FAIL] Should not have succeeded: {response}")

print("\n" + "=" * 60)
print("All Tests Completed Successfully!")
print("Room deletion constraint check is working correctly.")
print("=" * 60)