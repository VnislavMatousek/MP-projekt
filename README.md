![build status](../../actions/workflows/build.yml/badge.svg) ![coverage](./coverage.svg)

# Aplikace pro výpočet daně z příjmů fyzických osob

## Úvod

Vítejte v repozitáři naší aplikace pro výpočet daně z příjmů fyzických osob. Tato webová aplikace byla vytvořena s cílem zjednodušit a zpřístupnit proces výpočtu daně z příjmů pro širokou veřejnost v České republice. Aplikace je určena pro jednotlivce, kteří chtějí rychle, efektivně a správně vypočítat svou daňovou povinnost.

## Funkcionalita

Aplikace nabízí následující funkce:

- **Výpočet daně z příjmů:** Umožňuje uživatelům vypočítat výši daně na základě různých druhů příjmů.
- **Přehledné uživatelské rozhraní:** Nabízí jednoduché a intuitivní ovládání pro všechny uživatele.
- **Podpora různých typů příjmů:** Umožňuje zahrnout různé typy příjmů a odpočtů pro co nejpřesnější výpočet.
- **Aktualizované daňové tabulky:** Zahrnuje nejnovější daňové sazby a úlevy.

## Technologie

Aplikace je vyvinuta s využitím moderních technologií:

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **Backend:** Django (Python)
- **Databáze:** SQLite

## Instalace

Pro spuštění aplikace na lokálním stroji postupujte podle následujících kroků:

1. Klonujte repozitář do vašeho lokálního stroje:
   
   git clone https://github.com/vaseGithubUzivatelskeJmeno/aplikace-dane.git

2. Přejděte do složky s projektem:

   cd MP-Projekt
   
3. Nainstalujte potřebné závislosti:

   pip install -r requirements.txt

4. Spusťte Django server:

   docker compose up


Po spuštění serveru je aplikace dostupná na `http://127.0.0.1:8000/`.

## Použití

Po spuštění aplikace můžete přistoupit k výpočtu vaší daně z příjmů. Stačí zadat relevantní informace do formuláře a aplikace vypočítá vaši daňovou povinnost.

## Přispění

Jsme otevřeni jakýmkoliv připomínkám nebo příspěvkům. Pokud máte návrh na vylepšení nebo jste našli chybu, neváhejte vytvořit nový issue nebo pull request.

## Licence

Tento projekt je distribuován pod [MIT licencí](LICENSE).

## Poděkování

Děkujeme všem přispěvatelům a uživatelům této aplikace a těšíme se na vaše návrhy a připomínky.
