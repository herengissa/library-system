# Guide för grupparbete

Här är hur vi jobbar tillsammans på projektet.

## 1. Lägg till klasskamrater på GitHub

### Viktigt om privata/publika repos

**Om repot är PRIVAT:**
- De kan se det om du lägger till dem som Collaborators
- De kan INTE se det om de bara är i Projects
- Projects och repo-behörigheter är olika saker!

**Om repot är PUBLIKT:**
- Alla kan se koden (det är publikt)
- Men de kan INTE pusha om de inte är Collaborators
- Lägg till dem som Collaborators så kan de pusha

**Kort sagt:** För att de ska kunna pusha måste de vara Collaborators på repot, oavsett om det är privat eller publikt.

### Så här lägger du till Collaborators

1. Gå till repot på GitHub
2. Klicka på **Settings**
3. Klicka på **Collaborators** i vänstermenyn
4. Klicka **Add people**
5. Sök efter deras GitHub-användarnamn eller email
6. Ge dem **Write**-behörighet
7. De får en email som de måste acceptera

**OBS:** Om repot är privat måste de acceptera inbjudan först!

### GitHub Projects

Projects delas automatiskt när de har access till repot. De kan då se Project Board, lägga till issues, etc.

## 2. Klona repot (för klasskamrater)

**Mac/Linux:**
```bash
git clone https://github.com/herengissa/library-system.git
cd library_system
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows/PC:**
```cmd
git clone https://github.com/herengissa/library-system.git
cd library_system
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Glöm inte att skapa en `.env` fil med Render connection string!

## 3. Arbetssätt

### Så här jobbar vi med varje uppgift:

1. **Ta ett issue från "To do"**
   - Gå till Project Board
   - Välj ett issue du vill göra

2. **Skapa en branch**
   ```bash
   git checkout -b feature/issue-1-schema-sql
   ```

3. **Flytta issue till "In Progress"**
   - Dra issue-kortet i Project Board

4. **Jobba på uppgiften**
   - Gör dina ändringar
   - Testa att det fungerar

5. **Commit och push**
   ```bash
   git add .
   git commit -m "Lägger till schema.sql"
   git push origin feature/issue-1-schema-sql
   ```

6. **Skapa Pull Request**
   - Gå till GitHub → Pull requests → New pull request
   - Välj din branch
   - Lägg till beskrivning
   - Skapa PR

7. **Merge Pull Request**
   - När någon har kollat (eller direkt om ni litar på varandra)
   - Klicka "Merge pull request"

8. **Flytta issue till "Done"**
   - Dra issue-kortet i Project Board

9. **Uppdatera din lokala kod**
   ```bash
   git checkout main
   git pull origin main
   ```

## 4. Render-databasen

### Viktigt om Render

- Render är bara databasen - alla ansluter till samma databas
- Kod delas via GitHub, inte Render
- Alla ser samma data - när någon lägger till en bok ser alla den

### Connection string

Alla använder samma:
```
postgresql://bibliotekdb:JSI0NDRp9OrcUmROp4eFeM3Hh5TiFAvp@dpg-d4b3ejvgi27c73945jog-a.oregon-postgres.render.com:5432/bibliotekdb
```

### Verktyg

- **pgAdmin 4** - grafiskt, enkelt att använda
- **psql** - kommandorad, snabbt för SQL-filer
- **Python-appen** - för att testa funktioner

### Vem skapar tabellerna?

- Bara EN person behöver köra `schema.sql` (skapar tabellerna)
- Bara EN person behöver köra `testdata.sql` (lägger till testdata)
- Alla kan köra `queries.sql` (ingen skada om flera kör)

## 5. Synkronisera ändringar

### När någon pushar kod till GitHub

```bash
git checkout main
git pull origin main
```

Om du har lokala ändringar:
```bash
git stash
git pull origin main
git stash pop
```

### När någon ändrar databasen

**Data-ändringar (lägga till böcker, medlemmar, etc.):**
- Inget behöver göras - alla ser ändringarna direkt i Render

**Struktur-ändringar (lägga till kolumner, tabeller, etc.):**
- MÅSTE uppdatera `database/schema.sql` på GitHub!
- Commita och pusha schema.sql så att alla har samma struktur

**Exempel:**
Om du lägger till en kolumn i pgAdmin:
```sql
ALTER TABLE books ADD COLUMN description TEXT;
```

Då måste du också uppdatera `database/schema.sql`:
```sql
CREATE TABLE books (
    ...
    description TEXT,
    ...
);
```

Sen commita och pusha:
```bash
git add database/schema.sql
git commit -m "Lägger till description-kolumn i books"
git push
```

## 6. Best Practices

### Gör:
- Commita ofta med tydliga meddelanden
- Använd branches för varje issue
- Testa innan du pushar
- Pull senaste ändringar innan du börjar jobba

### Undvik:
- Pusha direkt till main (använd branches!)
- Glömma att commita
- Jobba på samma fil samtidigt (prata med varandra)
- Glömma att uppdatera schema.sql vid strukturändringar

## 7. Om något går fel

**"Permission denied" när du pushar:**
- Kolla att du är collaborator
- Kolla att du är inloggad på GitHub

**"Database connection failed":**
- Render kan gå i "sleep mode" - vänta några sekunder
- Kolla att .env-filen har rätt värden

**Merge conflicts:**
- När flera ändrar samma fil
- Lös konflikterna manuellt i filen
- Sen: `git add .`, `git commit -m "Fixar merge conflicts"`, `git push`

## 8. Checklist för nya i gruppen

- [ ] GitHub-konto
- [ ] Är collaborator i repot
- [ ] Har klonat repot
- [ ] Har .venv och installerat paket
- [ ] Har .env med Render connection string
- [ ] Har testat att Python-appen fungerar
- [ ] Kan se Project Board
- [ ] Förstår branches och Pull Requests
