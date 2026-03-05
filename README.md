# TicketPortal Ticket Checker & Reservation Script

Tento projekt je Python skript vytvořený jako experiment s automatizací HTTP komunikace a práci se sessions. Slouží k monitorování dostupnosti vstupenek na portálu **TicketPortal** a pokusu o jejich automatickou rezervaci při uvolnění míst.

Primárním cílem projektu bylo procvičit práci s přímou komunikací se serverem bez použití prohlížeče, pochopit strukturu requestů/responsí a vyzkoušet automatizaci procesu od kontroly dostupnosti až po vytvoření objednávky.

---

# 🚀 Hlavní funkce

**Monitoring dostupnosti vstupenek**  
Skript pravidelně odesílá HTTP požadavky na endpoint TicketPortal a kontroluje, zda jsou pro daný koncert dostupná místa.

**Automatické přidání do košíku**  
Jakmile jsou vstupenky dostupné, skript je automaticky přidá do košíku pomocí interních endpointů služby.

**Automatizovaný checkout**  
Po vytvoření košíku skript odešle POST request s potřebnými daty pro dokončení rezervace.

**Proxy podpora**  
Možnost rotace proxy serverů z externího souboru pro paralelní běh více tasků.

**Paralelní běh tasků**  
Každý task běží ve vlastním vlákně, což umožňuje sledovat více sektorů nebo koncertů současně.

**Logování**  
Barevné logy s časovou značkou pro přehled o stavu jednotlivých tasků.

**Discord notifikace**  
Při úspěšném checkoutu odešle skript automatické oznámení na Discord webhook s informacemi o eventu.

**Ukládání výsledků**  
Úspěšné rezervace jsou ukládány do CSV souboru pro pozdější kontrolu.

---

# 🛠 Použité technologie

- Python 3.x  
- Requests (HTTP komunikace a session management)  
- Threading (paralelní běh tasků)  
- CSV (načítání tasků a ukládání výsledků)  
- Discord Webhooks (notifikace)  
- Colorama (barevné logování v terminálu)
