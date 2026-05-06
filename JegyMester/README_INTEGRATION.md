# JegyMester frontend-backend összekötés

Ez a csomag egy kibővített React frontendet tartalmaz, amely már a backend fő funkcióit használja.

## Backend indítás

```powershell
cd C:\jegymester\Jegymester_AUTH
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Első indítás előtt hozd létre az adatbázist és az alap szerepköröket:

```powershell
python init_db.py
```

Opcionális demo adatokkal is feltöltheted:

```powershell
python seed_demo.py
```

Backend indítása:

```powershell
python run_app.py
```

Backend URL: `http://localhost:8888`
Swagger: `http://localhost:8888/swagger`
API base URL: `http://localhost:8888/api`

## Frontend indítás

Másik PowerShell ablakban:

```powershell
cd C:\jegymester\jegymester_full_frontend
npm install
npm start
```

Frontend URL: `http://localhost:3000`

## Elkészült frontend funkciók

### Auth

- Regisztráció: `POST /api/users/register`
- Belépés: `POST /api/users/login`
- Bejelentkezett felhasználó lekérése: `GET /api/users/me`
- Token automatikus küldése `Authorization: Bearer ...` headerben

### Jegyvásárló oldal

- Vetítések listázása: `GET /api/screenings/`
- Filmek listázása: `GET /api/movies/`
- Termek listázása: `GET /api/rooms/`
- Székek lekérése vetítéshez: `GET /api/seats/:screeningId`
- Több szék foglalása: `POST /api/tickets/reserve`

### Admin oldal

- Filmek: lista, hozzáadás, szerkesztés, törlés
- Termek: lista, hozzáadás, törlés
- Vetítések: lista, hozzáadás, törlés
- Székek: lista, hozzáadás, törlés
- Jegyek: lista, hozzáadás, törlés
- Tranzakciók: lista, hozzáadás, törlés
- Szerepkörök: lista, hozzáadás, törlés

## Fontos backend javítások

- `app/__init__.py`: javítva az `import app.blueprints` névütközés.
- `user/service.py`: fejlesztői környezethez a JWT token `HS256` algoritmussal készül, így nem kötelező a `private-key.pem`.
- `init_db.py`: gyors adatbázis-inicializáló script.
- `seed_demo.py`: gyors demo adatfeltöltő script.

## Ajánlott első próba

```powershell
cd C:\jegymester\Jegymester_AUTH
python init_db.py
python seed_demo.py
python run_app.py
```

Másik ablakban:

```powershell
cd C:\jegymester\jegymester_full_frontend
npm install
npm start
```

Ezután nyisd meg: `http://localhost:3000`

Regisztrálj egy új felhasználót, majd a Jegyvásárlás oldalon ki tudod próbálni a demo vetítést és a székfoglalást.
