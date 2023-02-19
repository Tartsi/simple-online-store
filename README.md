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

## Välipalautus 3

- Pieni huomio tähän välipalautukseen on käden sormivamma joka esti minua edistämästä sovellusta haluamaani määrää.

- Sovelluksen nykyinen tilanne (19.02.2023) tarjoaa mahdollisuuden tuotteiden arvioimiseen, arviointien selaamiseen, sekä admin-tason käyttäjille mahdollisuuden poistaa käyttäjiä ja tuotteita. Lopulliseen palautukseen jää ostoskorin ja maksutapahtuman toteuttaminen, sekä mahdolliset toiminnallisuudet joita ehdotetaan palautteessa. Muitakin parannuksia yleisellä tasolla.

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

- Luo sovelluksen tietokantataulut skeemaasi tables.sql-tiedostosta
- HUOM! Tietokantaan on tullut muutoksia Välipalautus 2-vaiheesta. Uudelleenalustus on välttämätöntä.

- Luo ylläpitäjä-tason käyttäjä rekisteröitymis-sivulta hyödyntäen admin-salasanaa, joka löytyy routse.py-tiedoston alusta:

```
my_admin_password = "admin123" (esim.)
```

![Admin](images/register-admin.png "Admin registration")

- Ylläpitäjä-tason käyttäjä tarvitaan tuotteiden lisäämiseen tietokantaan.

- Käynnistä sovellus ajamalla routes.py-tiedoston koodi.

- Voit halutessasi kokeilla tietokanta yhteyttä "paikallinenosoite/testdatabase" linkin kautta.
