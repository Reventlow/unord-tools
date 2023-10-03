# UnordToolsProject
Det er et udlaans system og asset management system til U/NORD.

## Introduktion
Dette er en Django 3.2.3 webapplikation med flere indbyggede og tredjeparts applikationer. Projektet er konfigureret til at køre både lokalt og i produktion.

## Forudsætninger
- Python 3.9
- Django 3.2.3
- Postgresql eller SQLite (afhængig af din konfiguration)


### Database
Standardindstillingen bruger SQLite. Men Heroku konverter de indstillinger til Postgresql.

### AWS S3
Projektet er sat op til at bruge AWS S3 til at håndtere statiske og mediefiler. For at sætte dette op:
- Tilføj `AWS_ACCESS_KEY_ID` og `AWS_SECRET_ACCESS_KEY` til din `.env` fil.
- Ændre `AWS_STORAGE_BUCKET_NAME` og `AWS_S3_CUSTOM_DOMAIN` som nødvendigt.

### Tredjeparts Apps
- **REST Framework**: Til API'er.
- **TinyMCE**: For WYSIWYG redigering.
- **Easy PDF**: Til PDF generering.

## Køre Projektet lokalt
1. Anvend `python manage.py migrate` til at anvende database migreringer.
2. Kør serveren med `python manage.py runserver`.

>[!Warning]
> Projektet er konfigureret til at køre med SQLite som standard. Hvis du vil bruge Postgresql, skal du ændre `DATABASES` i `settings.py` filen.


## Produktion
I en produktionssituation, skal du sørge for at:
- Sætte `DEBUG = False`
- Tilføje dit domæne til `ALLOWED_HOSTS`

## Drift
Projektet bliver driftet på Heroku. For at deploye til Heroku.

## Teknologier Brugt
- Python
- Django
- AWS S3
- REST Framework
- TinyMCE
- Easy PDF
