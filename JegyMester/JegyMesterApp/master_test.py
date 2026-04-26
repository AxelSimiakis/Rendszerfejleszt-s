import requests

BASE_URL = "http://localhost:8888/api"

def run_master_test():
    print("🚀 --- JEGYMESTER ATFOGO TESZT INDITASA --- 🚀\n")

    # ==========================================
    # 1. REGISZTRACIO ES LOGIN (TOKEN MEGSZERZESE)
    # ==========================================
    print("[1/6] Felhasznalo kezeles (Register & Login)...")
    
    user_payload = {
        "name": "Teszt Elek", 
        "email": "teszt@elek.hu", 
        "phone_number": "123", 
        "password": "pw"
    }

    # Regisztracio
    reg_res = requests.post(f"{BASE_URL}/users/register", json=user_payload)
    if reg_res.status_code == 201:
        print("✔️  Regisztracio sikeres.")
    else:
        print(f"ℹ️  Regisztracio kihagyva (valoszinuleg mar letezik a user).")

    # Bejelentkezes a tokenert
    login_res = requests.post(f"{BASE_URL}/users/login", json={
        "email": user_payload["email"], 
        "password": user_payload["password"]
    })
    
    if login_res.status_code != 200:
        print("❌ HIBA: Nem sikerult a bejelentkezes! Ellenorizd a verify_token-t a szerveren.")
        return

    token = login_res.json().get('token')
    headers = {"Authorization": f"Bearer {token}"}
    user_id = login_res.json().get('id')
    print(f"✔️  Login sikeres! Token megszerezve. User ID: {user_id}\n")

    # ==========================================
    # 2. ADATOK FELTOLTESE (Authorization fejlécet használva)
    # ==========================================
    print("[2/6] Adatok feltoltese (Terem, Szekek, Film, Vetites)...")
    
    room = requests.post(f"{BASE_URL}/rooms/", json={"name": "VIP Mini", "total_capacity": 2}, headers=headers).json()
    room_id = room.get('id')

    s1 = requests.post(f"{BASE_URL}/seats/", json={"room_id": room_id, "row_num": 1, "seat_num": 1}, headers=headers).json()
    s2 = requests.post(f"{BASE_URL}/seats/", json={"room_id": room_id, "row_num": 1, "seat_num": 2}, headers=headers).json()
    seat1_id, seat2_id = s1.get('id'), s2.get('id')

    movie = requests.post(f"{BASE_URL}/movies/", json={"title": "Teszt Matrix", "duration_minutes": 120}, headers=headers).json()
    screen = requests.post(f"{BASE_URL}/screenings/", json={"movie_id": movie.get('id'), "room_id": room_id, "start_time": "2026-10-10T20:00:00"}, headers=headers).json()
    screening_id = screen.get('id')

    print("✔️  Adatok sikeresen feltoltve!\n")

    # ==========================================
    # 3. LISTAZAS TESZTELESE
    # ==========================================
    print("[3/6] Aktualis vetitesek lekerdezese...")
    screenings_list = requests.get(f"{BASE_URL}/screenings/", headers=headers).json()
    print(f"✔️  Talalt vetitesek szama: {len(screenings_list)}\n")

    # ==========================================
    # 4. JEGY VASARLASA
    # ==========================================
    print("[4/6] Ket jegy megvasarlasa...")
    tx = requests.post(f"{BASE_URL}/transactions/", json={"user_id": user_id, "total_amount": 5000, "payment_method": "keszpenz"}, headers=headers).json()
    tx_id = tx.get('id')

    t1 = requests.post(f"{BASE_URL}/tickets/", json={"transaction_id": tx_id, "screening_id": screening_id, "seat_id": seat1_id}, headers=headers)
    t2 = requests.post(f"{BASE_URL}/tickets/", json={"transaction_id": tx_id, "screening_id": screening_id, "seat_id": seat2_id}, headers=headers)
    
    if t1.status_code == 201 and t2.status_code == 201:
         print("✔️  Jegyek lefoglalva!\n")
    else:
         print(f"❌  Hiba a jegyvasarlasnal! Kod: {t1.status_code}\n")

    # ==========================================
    # 5. DUPLA FOGLALAS TESZT
    # ==========================================
    print("[5/6] Teszt: Ugyanannak a szeknek a lefoglalasa megegyszer...")
    t_dup = requests.post(f"{BASE_URL}/tickets/", json={"transaction_id": tx_id, "screening_id": screening_id, "seat_id": seat1_id}, headers=headers)
    
    if t_dup.status_code == 400:
        print(f"✔️  TESZT SIKERES: A rendszer megallitotta a dupla foglalast.\n")
    else:
        print(f"❌  TESZT ELBUKOTT: A rendszer engedte a dupla foglalast! Kod: {t_dup.status_code}\n")

    print("🎉 --- MINDEN TESZT LEFUTOTT! --- 🎉")

if __name__ == "__main__":
    try:
        run_master_test()
    except requests.exceptions.ConnectionError:
        print("Hiba: Nem fut a Flask szerver!")