# Library Management System

**Kurs:** Databasteknik PIA25  
**Gruppuppgift:** Databassystem för ett bibliotek

Ett databassystem för bibliotek som hanterar böcker, medlemmar och lån. Systemet består av en PostgreSQL-databas och en Python-konsolapplikation.

## Projektstruktur

```
library_system/
├── database/
│   ├── schema.sql           # Databasschema
│   ├── testdata.sql         # Testdata
│   └── queries.sql          # Alla SQL-queries
├── src/
│   ├── __init__.py
│   ├── main.py             # Huvudprogram med meny
│   ├── database.py         # Databasanslutning
│   ├── book_manager.py     # Bokhantering
│   ├── member_manager.py   # Medlemshantering
│   └── loan_manager.py     # Lånehantering
├── requirements.txt        # Python-paket
├── README.md              # Denna fil
└── .gitignore             # Git ignore-filer
```

## Installation

### 1. Klona repot

```bash
git clone <repository-url>
cd library_system
```

### 2. Skapa virtuell miljö

```bash
python3 -m venv .venv
source .venv/bin/activate  # På Windows: .venv\Scripts\activate
```

### 3. Installera dependencies

```bash
pip install -r requirements.txt
```

### 4. Konfigurera databas

1. Skapa en PostgreSQL-databas:
   ```sql
   CREATE DATABASE library_db;
   ```

2. Sätt miljövariabler (eller skapa en `.env` fil):
   ```bash
   export POSTGRES_DB=library_db
   export POSTGRES_USER=postgres
   export POSTGRES_PASSWORD=ditt_lösenord
   export POSTGRES_HOST=localhost
   export POSTGRES_PORT=5432
   ```

3. Kör schema och testdata:
   ```bash
   psql -U postgres -d library_db -f database/schema.sql
   psql -U postgres -d library_db -f database/testdata.sql
   ```

## Användning

Kör applikationen:

```bash
python -m src.main
```

Eller om du är i `src/` mappen:

```bash
python main.py
```

## Funktioner

### Bokhantering
- Visa alla böcker
- Sök efter bok (titel eller författare)
- Lägg till ny bok
- Visa tillgängliga böcker

### Medlemshantering
- Visa alla medlemmar
- Lägg till ny medlem
- Sök efter medlem (namn eller email)

### Lånehantering
- Registrera nytt lån
- Registrera återlämning
- Visa aktiva lån
- Visa försenade lån

### Statistik och rapporter
- Visa mest lånade böcker
- Visa medlem med flest lån
- Visa översikt av biblioteket

## SQL Queries

Alla SQL-queries finns i `database/queries.sql` och inkluderar:
- Grundläggande SELECT-queries
- JOIN-queries
- Aggregering och analys

## Grupparbete med GitHub Projects

För att använda GitHub Projects för att organisera arbetet:

1. Gå till ditt GitHub-repo
2. Klicka på "Projects" i repots meny
3. Skapa ett nytt Project board
4. Skapa kolumner för: "To Do", "In Progress", "Review", "Done"
5. Skapa issues för varje uppgift och lägg till dem i projektet

## Bidrag

Varje gruppmedlem bör:
- Skapa en egen branch för sina ändringar
- Commita ofta med beskrivande meddelanden
- Skapa pull requests för review
- Testa sina ändringar innan merge

## Licens

Detta projekt är en del av kursen Databasteknik PIA25.

