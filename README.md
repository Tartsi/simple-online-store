# Nettikauppasovellus

Sovelluksen avulla tavallinen käyttäjä voi kirjautua palveluun, selata kaupassa olemassa olevia tuotteita, lisätä tuotteita ostoskoriin, arvostella tuotteita ja halutessa täyttää tilaustiedot ja läpikäydä teko-maksutapahtuman. Ylläpitäjä voi lisätä/poistaa nettikauppan tuotteita, lisätä nykyisten tuotteiden varastoa ja muunnella esimerkiksi hintoja tai tuotekuvausta.

Ominaisuuksiin lukeutuu alustavasti:

- Rekisteröityminen ja kirjautuminen.
- Nettikaupan saatavilla olevien tuotteiden selaaminen ja lisääminen ostoskoriin.
- Teko-maksutapahtuma ja tilauksen käsittely.
- Tuotearvostelut.
- Ostoshistorian selaaminen.

Alustava tietokantataulurakenne:

- Taulu käyttäjien dataan (mukaanlukien ylläpito)
- Taulu tuotedataan
- Taulu ostoskärrylle
- Taulu käsitellyille ostoksille/tilauksille
- Taulu tuotearvosteluille

## Välipalautus 2

- Sovelluksen nykyinen tilanne (05.02.2023) tarjoaa mahdollisuuden rekisteröitymiseen, sisäänkirjautumiseen, tuotteiden selaamiseen ja etsimiseen ja ylläpitäjä-tason käyttäjille mahdollisuuden uusien tuotteiden lisäämiseen ja nykyisten tuotteiden varaston lisäämiseen.

### Ohjeet testaamiseen

- Kloonaa kansio ja siirry juurikansioon, minkä jälkeen luo .env-tiedosto, johon määrität käyttämäsi paikallisen tietokannan ja salaisen avaimen:

```
DATABASE_URL = käyttämä tietokantasi
SECRET_KEY = käyttämä salainen avaimesi
```

- Aktivoi halutessasi virtuaaliympäristö, jonka jälkeen lataa vaaditut riippuvuudet:

```
pip install -r ./project-dependencies.txt
```

- Luo sovelluksen tietokanta-skeema esimerkiksi kopioimalla tiedoston tables.sql-sisältö ja ajamalla se komentokehotteessa.

- Luo ylläpitäjä-tason käyttäjä manuaalisesti suoraan tietokantaan komennolla:

```
INSERT INTO users (username, password, admin) VALUES ('admin', 'salasanasi', 1);
```

- Väliaikaisesti tämä on ainoa tapa lisätä ylläpitäjä-tason käyttäjä sovellukseen. Ylläpitäjä-tason käyttäjä tarvitaan tuotteiden lisäämiseen tietokantaan.

- Käynnistä sovellus ajamalla routes.py-tiedoston koodi.

- Voit halutessasi kokeilla tietokanta yhteyttä "osoite/testdatabase" linkin kautta.
