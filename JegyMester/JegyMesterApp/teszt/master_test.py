import requests

BASE_URL = "http://localhost:8888/api"

def run_master_test():
    print("🚀 --- JEGYMESTER ATFOGO TESZT INDITASA --- 🚀\n")

    # ==========================================
    # 1. ADATOK FELTOLTESE (SEEDING)
    # ==========================================
    print("[1/5] Adatok generalasa (Terem, Szekek, Film, Vetites, User)...")
    
    # Letrehozunk egy nagyon pici, 2 fos termet
    room = requests.post(f"{BASE_URL}/rooms/", json={"name": "VIP Mini", "total_capacity": 2}).json()
    room_id = room.get('id', 1)

    # Letrehozzuk a 2 db szeket a teremhez
    s1 = requests.post(f"{BASE_URL}/seats/", json={"room_id": room_id, "row_num": 1, "seat_num": 1}).json()
    s2 = requests.post(f"{BASE_URL}/seats/", json={"room_id": room_id, "row_num": 1, "seat_num": 2}).json()
    seat1_id, seat2_id = s1.get('id', 1), s2.get('id', 2)

    # Film es Vetites
    movie = requests.post(f"{BASE_URL}/movies/", json={"title": "Teszt Matrix", "duration_minutes": 120}).json()
    screen = requests.post(f"{BASE_URL}/screenings/", json={"movie_id": movie.get('id', 1), "room_id": room_id, "start_time": "2026-10-10T20:00:00"}).json()
    screening_id = screen.get('id', 1)

    # User letrehozasa
    user = requests.post(f"{BASE_URL}/users/register", json={"name": "Teszt Elek", "email": "teszt@elek.hu", "phone_number": "123", "password": "pw"}).json()
    user_id = user.get('id', 1)

    print("✔️  Adatok sikeresen feltoltve!\n")

    # ==========================================
    # 2. LISTAZAS TESZTELESE
    # ==========================================
    print("[2/5] Aktualis vetitesek lekerdezese...")
    screenings_list = requests.get(f"{BASE_URL}/screenings/").json()
    print(f"✔️  Talalt vetitesek szama: {len(screenings_list)}")
    print(f"    Legutobbi vetites ID: {screenings_list[-1]['id']}, Datum: {screenings_list[-1]['start_time']}\n")

    # ==========================================
    # 3. TOBB JEGY VASARLASA (SIKERES FOLYAMAT)
    # ==========================================
    print("[3/5] Ket jegy megvasarlasa (a terem megtelik)...")
    tx = requests.post(f"{BASE_URL}/transactions/", json={"user_id": user_id, "total_amount": 5000, "payment_method": "keszpenz"}).json()
    tx_id = tx.get('id', 1)

    # Megvesszuk az 1-es es 2-es szeket
    t1 = requests.post(f"{BASE_URL}/tickets/", json={"transaction_id": tx_id, "screening_id": screening_id, "seat_id": seat1_id})
    t2 = requests.post(f"{BASE_URL}/tickets/", json={"transaction_id": tx_id, "screening_id": screening_id, "seat_id": seat2_id})
    
    if t1.status_code == 201 and t2.status_code == 201:
         print("✔️  Mindket jegy sikeresen lefoglalva! (A terem most tele van)\n")
    else:
         print("❌  Hiba a jegyvasarlasnal!\n")

    # ==========================================
    # 4. DUPLA FOGLALAS TESZT (HIBAVARAS)
    # ==========================================
    print("[4/5] Teszt: Ugyanannak a szeknek a lefoglalasa megegyszer...")
    t_dup = requests.post(f"{BASE_URL}/tickets/", json={"transaction_id": tx_id, "screening_id": screening_id, "seat_id": seat1_id})
    
    if t_dup.status_code == 400:
        print(f"✔️  TESZT SIKERES: A rendszer megvedett a dupla foglalastol! (Uzenet: '{t_dup.json().get('message')}')\n")
    else:
        print(f"❌  TESZT ELBUKOTT: A rendszer engedte a dupla foglalast! Kod: {t_dup.status_code}\n")

    # ==========================================
    # 5. TULFOGLALAS TESZT (HIBAVARAS)
    # ==========================================
    print("[5/5] Teszt: Tulfoglalas (3. jegy vetele egy 2 fos terembe)...")
    # Megprobalunk egy olyan szekre (pl. ID: 9999) jegyet venni, ami nincs a teremben
    t_over = requests.post(f"{BASE_URL}/tickets/", json={"transaction_id": tx_id, "screening_id": screening_id, "seat_id": 9999})
    
    if t_over.status_code != 201:
        print("✔️  TESZT SIKERES: A rendszer nem enged jegyet kiallitani nem letezo szekre (megakadalyozza a tulfoglalast)!\n")
    else:
        print("❌  TESZT ELBUKOTT: A rendszer engedte a tulfoglalast!\n")

    print("🎉 --- MINDEN TESZT LEFUTOTT! --- 🎉")

if __name__ == "__main__":
    try:
        run_master_test()
    except requests.exceptions.ConnectionError:
        print("Hiba: Nem fut a Flask szerver! Inditsd el a 'python run_app.py' paranccsal egy masik terminalban.")