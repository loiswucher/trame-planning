# Trame de planning 12h – janvier à mars 2027

Trame de roulement jour/nuit en 12 h pour 60 agents, du 1er janvier au 31 mars 2027 : 10 postes de jour et 7 postes de nuit chaque jour. Les noms des agents sont fictifs (Agent 01 à 60).

## Fichiers
- `Trame_planning_12h_janv-mars_2027.xlsx` : onglet Synthèse (hypothèses, roulements complets, couverture) et onglet Trame (60 agents × 90 jours, codes J / N / R calculés par formules).
- `calendrier_agents.html` : calendrier par agent, à ouvrir dans un navigateur.
- `ics/` : un fichier .ics par agent (jour 7h-19h, nuit 19h-7h) à importer dans un agenda.
- `scripts/` : scripts Python qui génèrent la trame (voir ci-dessous).

## Hypothèses
- 38 agents à 100 %, 20 à 80 %, 2 à 50 %. 4 agents à 100 % font uniquement des jours (cycle JJRRR).
- 100 % : 1 jour, 1 nuit, 3 repos (5 jours). Roulement complet : 35 jours.
- 80 % : 4 blocs 1 jour / 1 nuit / 3 repos + 2 jours isolés sur 4 semaines, 4 nuits maximum par mois, peu de week-ends. Roulement complet : 28 jours.
- 50 % : 1 jour, 1 nuit, 8 repos (10 jours). Roulement complet : 70 jours.
- La trame ne tient pas compte des jours fériés ni des congés.

## Régénérer
Dans le dossier `scripts/` : `python3 opt80b.py 4 2` (candidats 80 %), `python3 milpZ.py 2 4 4_2` (affectation optimale), puis `python3 trame2.py`, `python3 build.py` (Excel) et `python3 cal.py` (page et .ics). Le fichier `milpZ_2_4_4_2.json` contient l'affectation retenue. Dépendances : openpyxl, numpy, scipy.
