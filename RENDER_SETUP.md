# Ansluta till Render-databasen

Här är hur du ansluter till vår delade Render-databas.

## Installera python-dotenv

Först behöver du installera python-dotenv så att vi kan läsa från .env-filen.

**Mac/Linux:**
```bash
cd /Users/Hereng/library_system
source .venv/bin/activate
pip install python-dotenv
```

**Windows/PC:**
```cmd
cd C:\Users\DittAnvändarnamn\library_system
.venv\Scripts\activate
pip install python-dotenv
```

## Testa anslutningen med psql

Testa att du kan ansluta:

**Mac/Linux:**
```bash
psql "postgresql://bibliotekdb:JSI0NDRp9OrcUmROp4eFeM3Hh5TiFAvp@dpg-d4b3ejvgi27c73945jog-a.oregon-postgres.render.com:5432/bibliotekdb"
```

**Windows/PC:**
```cmd
psql "postgresql://bibliotekdb:JSI0NDRp9OrcUmROp4eFeM3Hh5TiFAvp@dpg-d4b3ejvgi27c73945jog-a.oregon-postgres.render.com:5432/bibliotekdb"
```

Om det inte funkar på Windows, prova med fullständig sökväg:
```cmd
"C:\Program Files\PostgreSQL\17\bin\psql.exe" "postgresql://bibliotekdb:JSI0NDRp9OrcUmROp4eFeM3Hh5TiFAvp@dpg-d4b3ejvgi27c73945jog-a.oregon-postgres.render.com:5432/bibliotekdb"
```

Lösenordet är: `JSI0NDRp9OrcUmROp4eFeM3Hh5TiFAvp`

Om det fungerar, skriv `\q` för att avsluta.

## Ansluta med pgAdmin 4

pgAdmin är ett grafiskt verktyg - mycket enklare att använda än psql om du inte gillar terminalen.

### Installera pgAdmin 4

1. Ladda ner från: https://www.pgadmin.org/download/
2. Installera som vanligt

### Skapa anslutning

1. Öppna pgAdmin 4
2. Högerklicka på "Servers" → "Register" → "Server..."
3. I "General"-fliken: ge den ett namn (t.ex. "Render Database")
4. I "Connection"-fliken:
   - **Host:** `dpg-d4b3ejvgi27c73945jog-a.oregon-postgres.render.com`
   - **Port:** `5432`
   - **Database:** `bibliotekdb`
   - **Username:** `bibliotekdb`
   - **Password:** `JSI0NDRp9OrcUmROp4eFeM3Hh5TiFAvp`
   - ✅ Kryssa i "Save password"
5. Klicka "Save"

Nu kan du se tabeller, köra queries, och allt annat direkt i gränssnittet!

## Skapa tabellerna

Kör schema.sql mot Render-databasen:

**Mac/Linux:**
```bash
psql "postgresql://bibliotekdb:JSI0NDRp9OrcUmROp4eFeM3Hh5TiFAvp@dpg-d4b3ejvgi27c73945jog-a.oregon-postgres.render.com:5432/bibliotekdb" -f database/schema.sql
```

**Windows/PC:**
```cmd
psql "postgresql://bibliotekdb:JSI0NDRp9OrcUmROp4eFeM3Hh5TiFAvp@dpg-d4b3ejvgi27c73945jog-a.oregon-postgres.render.com:5432/bibliotekdb" -f database\schema.sql
```

**Viktigt:** Detta tar bort alla befintliga tabeller! Prata med gruppen först om någon redan har skapat tabeller.

## Lägg till testdata

**Mac/Linux:**
```bash
psql "postgresql://bibliotekdb:JSI0NDRp9OrcUmROp4eFeM3Hh5TiFAvp@dpg-d4b3ejvgi27c73945jog-a.oregon-postgres.render.com:5432/bibliotekdb" -f database/testdata.sql
```

**Windows/PC:**
```cmd
psql "postgresql://bibliotekdb:JSI0NDRp9OrcUmROp4eFeM3Hh5TiFAvp@dpg-d4b3ejvgi27c73945jog-a.oregon-postgres.render.com:5432/bibliotekdb" -f database\testdata.sql
```

## Testa Python-appen

Nu ska allt fungera! Kör:

```bash
python -m src.main
```

## Om något inte fungerar

**Anslutningen funkar inte:**
- Render-databasen kan gå i "sleep mode" - vänta några sekunder och försök igen
- Kontrollera att connection string är rätt
- Kolla att .env-filen finns och har rätt värden

**Python kan inte ansluta:**
- Kontrollera att python-dotenv är installerat: `pip list | grep dotenv` (Mac) eller `pip list | findstr dotenv` (Windows)
- Kolla att .env-filen finns i projektets root-mapp

**Windows-problem:**
- Om `psql` inte hittas, lägg till PostgreSQL i PATH eller använd fullständig sökväg
- Använd backslash (`\`) i sökvägar på Windows
