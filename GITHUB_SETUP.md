# Instruktioner för att pusha kod till GitHub

Efter att du har skapat repot på GitHub, kör dessa kommandon i terminalen:

### Mac/Linux:
```bash
cd /Users/Hereng/library_system

# Initiera Git (om inte redan gjort)
git init

# Lägg till alla filer
git add .

# Gör första commit
git commit -m "Initial commit: Library Management System"

# Lägg till GitHub remote (byt ut <användarnamn> mot ditt GitHub-användarnamn)
git remote add origin https://github.com/herengissa/library-system.git

# Pusha till GitHub
git branch -M main
git push -u origin main
```

### Windows/PC:
```cmd
cd C:\Users\DittAnvändarnamn\library_system

# Initiera Git (om inte redan gjort)
git init

# Lägg till alla filer
git add .

# Gör första commit
git commit -m "Initial commit: Library Management System"

# Lägg till GitHub remote (byt ut <användarnamn> mot ditt GitHub-användarnamn)
git remote add origin https://github.com/herengissa/library-system.git

# Pusha till GitHub
git branch -M main
git push -u origin main
```

Om du redan har ett repo och behöver pusha ändringar:

**Mac/Linux:**
```bash
git add .
git commit -m "Beskrivning av ändringar"
git push
```

**Windows/PC:**
```cmd
git add .
git commit -m "Beskrivning av ändringar"
git push
```

