<div align="center">

# Business-Prognosis

### Zeitreihen-Prognose – Hochschule Aalen, SS 2026

![Hochschule Aalen](https://img.shields.io/badge/Hochschule%20Aalen-SS%202026-8A2BE2)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)

</div>

---

Dieses Repository bündelt die Kursmaterialien und das Capstone-Projekt zur **Business-Prognosis**.
Es besteht aus zwei Teilen: den **Tutorials** zu den beiden Prognose-Verfahren
(**Prophet** und **Chronos**, jeweils auf denselben Rossmann-Daten) und dem eigenständigen
**Capstone-Projekt** (PM2.5-Luftqualitätsprognose für Beijing).

## Ordnerstruktur (Wurzelverzeichnis)

| Ordner | Inhalt |
|:---|:---|
| [`prophet/`](prophet/) | **Prophet-Tutorial** für die Studierenden: Demo-, Hands-On- und Musterlösungs-Notebooks, Rossmann-Daten, Fachliteratur und Einstiegspräsentation. |
| [`chronos/`](chronos/) | **Chronos-Tutorial** (Foundation Model): Demo-, Hands-On- und Musterlösungs-Notebooks, Rossmann-Daten, Literatur und Präsentation. |
| [`Capstone Projekt/`](Capstone%20Projekt/) | Das **eigentliche Projekt**: PM2.5-Prognose Beijing mit Prophet, Chronos und TFT – Notebooks, Daten, Grafiken, Modelle, Dashboard und Präsentation. Eigenes README im Ordner. |
| [`docs/`](docs/) | **GitHub-Pages-Website**: das PM2.5-Dashboard als `index.html`, öffentlich abrufbar (siehe unten). |

## Dateien im Wurzelverzeichnis

| Datei | Zweck |
|:---|:---|
| `README.md` | Diese Übersicht. |

## Die einzelnen Ordner im Detail

### `prophet/`
Tutorial zum klassischen Prognose-Modell **Prophet**.

- `notebooks/` – `1_prophet_demo_final.ipynb` (Demo), `2_prophet_handson_students.ipynb` (Aufgaben zum Selbermachen), `3_prophet_handson_solution.ipynb` (Musterlösung) sowie erklärende Bilder.
- `data/` – Beispieldaten (`flights.csv`, Rossmann-Store-Sales).
- `literature/` – wissenschaftliche Papers zu Prophet und NeuralProphet.
- `images/` – Illustrationen für die Notebooks.
- `powerpoint/` – Einstiegspräsentation zu Prophet.
- `README.md` / `ts-tutorial.yml` – Setup-Anleitung und Conda-Umgebung.

### `chronos/`
Tutorial zum **Chronos** Foundation Model (vortrainiertes Zeitreihen-Modell von Amazon).

- `notebooks/` – `1_chronos_demo.ipynb`, `2_chronos_handson_students.ipynb`, `3_chronos_handson_solution.ipynb`, plus `Airpassengers.ipynb` als Zusatzbeispiel.
- `data/`, `literature/`, `images/`, `presentation/` – analog zum Prophet-Ordner: Daten, Papers, Bilder und die Chronos-Präsentation.
- `README.md` / `ts-tutorial.yml` – Setup-Anleitung und Conda-Umgebung.

### `Capstone Projekt/`
Das durchgehende Anwendungsprojekt: Vorhersage der **PM2.5-Feinstaubwerte in Beijing**
mit Prophet, Chronos und einem Temporal Fusion Transformer (TFT). Enthält Daten,
Notebooks, Ergebnis-Grafiken, trainierte Modelle, ein interaktives Dashboard und die
Abschlusspräsentation. Eine detaillierte Ordnerbeschreibung steht im
[eigenen README](Capstone%20Projekt/README.md).

### `docs/`
Der Ordner, aus dem **GitHub Pages** die Website ausliefert.

- `index.html` – das komplette PM2.5-Dashboard (eigenständige Datei, keine externen Abhängigkeiten).
- `.nojekyll` – schaltet die Jekyll-Verarbeitung ab, damit die Datei unverändert ausgeliefert wird.
- `README.md` – Kurzanleitung zum Aktualisieren und Aktivieren der Seite.

**Live-Dashboard:** https://bettina2805.github.io/AIForBusinessPrognosis_fv/
*(Wird erst erreichbar, sobald GitHub Pages in den Repo-Einstellungen aktiviert ist: Settings → Pages → Deploy from a branch → `main` / `/docs`.)*

## Setup

Prophet- und Chronos-Tutorial haben jeweils ein eigenes README und eine eigene
Conda-Umgebung (`ts-tutorial.yml`). Das Capstone-Projekt bringt seine eigene
Umgebung mit (siehe [Capstone-README](Capstone%20Projekt/README.md)).
</content>
</invoke>
