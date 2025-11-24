# Bibliotekssystem

**Kurs:** Databasteknik PIA25  
**Gruppuppgift:** Databassystem för ett bibliotek

Ett enkelt bibliotekssystem som hanterar böcker, medlemmar och lån. Byggt med PostgreSQL och Python.

## Projektstruktur

```
library_system/
├── database/
│   ├── schema.sql           # Databasschema
│   ├── testdata.sql         # Testdata
│   └── queries.sql          # SQL-queries
├── src/
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # Databasanslutning
│   ├── main.py              # Huvudprogram
│   ├── book_manager.py      # Bokhantering
│   ├── member_manager.py    # Medlemshantering
│   └── loan_manager.py      # Lånehantering
├── requirements.txt         # Python-paket
└── README.md                # Denna fil
```

## Installation

### 1. Klona repot

```bash
git clone <repository-url>
cd library_system
```

### 2. Skapa virtuell miljö

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows/PC:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Installera paket

```bash
pip install -r requirements.txt
```

### 4. Sätt upp databasen

1. Skapa en PostgreSQL-databas:
   ```sql
   CREATE DATABASE library_db;
   ```

2. Skapa en `.env` fil i projektets root:
   ```
   POSTGRES_DB=library_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=ditt_lösenord
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

3. Kör schema och testdata:

   **Mac/Linux:**
   ```bash
   psql -U postgres -d library_db -f database/schema.sql
   psql -U postgres -d library_db -f database/testdata.sql
   ```

   **Windows/PC:**
   ```cmd
   psql -U postgres -d library_db -f database\schema.sql
   psql -U postgres -d library_db -f database\testdata.sql
   ```

## Kör programmet

```bash
python -m src.main
```

## Funktioner

- **Bokhantering:** Visa, sök, lägg till böcker
- **Medlemshantering:** Visa, sök, lägg till medlemmar
- **Lånehantering:** Registrera lån och återlämningar
- **Statistik:** Se mest lånade böcker, försenade lån, etc.

## SQL Queries

Alla queries finns i `database/queries.sql` - både enkla SELECT-queries och mer avancerade med JOIN och aggregering.

## Grupparbete

Se `COLLABORATION_GUIDE.md` för instruktioner om hur man jobbar tillsammans med GitHub.
