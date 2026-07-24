<div align="center">

# Capstone Projekt

### Business-Prognosis – Hochschule Aalen, SS 2026

![Hochschule Aalen](https://img.shields.io/badge/Hochschule%20Aalen-SS%202026-8A2BE2)

</div>

---

Dieser Ordner enthält das **Capstone-Projekt** zum Kurs Business-Prognosis:
die Vorhersage der **PM2.5-Feinstaubbelastung in Beijing** mit **Prophet**, **Chronos**
und einem **Temporal Fusion Transformer (TFT)**, inklusive Modellvergleich, Dashboard
und Abschlusspräsentation.

## Ordnerstruktur

| Ordner | Inhalt |
|:---|:---|
| `notebooks_fv/` | **Aktueller Arbeitsstand** – die finalen, gepflegten Notebooks der gesamten Pipeline (siehe unten). Hier wird gearbeitet. |
| `data/` | Alle Daten: Rohdaten der Beijing-Messstationen, aufbereitete Trainings-/Testdaten und die Ergebnis-CSVs der Modellläufe. |
| `grafiken/` | Ausgabe-Grafiken der Notebooks (Vergleichsplots, Konfidenzintervalle, Karten, Boxplots …) – Quelle für Präsentation und Dashboard. |
| `models/` | Trainierte TFT-Modelle (mehrere Versionen `tft_final_multivariat*`). |
| `dashboard/` | Interaktives HTML-Dashboard und das Build-Skript, das es erzeugt. |
| `presentation/` | Abschlusspräsentation (`Luftverschmutzung in Bejing.pptx`). |
| `literature/` | Fachliteratur/Papers zur PM2.5-Prognose in Beijing (Transformer, Multi-Site-Modelle …). |
| `images/` | Bilder für Präsentation und Dokumentation (Karten, Illustrationen). |
| `notebooks_artefakte/` | **Archiv** – ältere Notebook-Versionen, Backups und Zwischenstände. Nicht der aktive Arbeitsstand. |

## Dateien im Projektordner

| Datei | Zweck |
|:---|:---|
| `CRISP-DM-Projektplan_PM25_Beijing.docx` | Projektplan nach dem CRISP-DM-Vorgehensmodell. |
| `project_description.PDF` | Ursprüngliche Aufgabenstellung. |
| `ts-tutorial.yml` | Conda-Umgebung für Prophet + Chronos + TFT (siehe unten). |
| `tft.yml` / `chronos_env.yml` | Zusätzliche/alternative Umgebungsdefinitionen. |
| `README.md` | Diese Übersicht. |

## Die einzelnen Ordner im Detail

### `notebooks_fv/` – aktueller Arbeitsstand
Die durchnummerierte Pipeline von der Datenanalyse bis zum Modellvergleich:

- `01_Datenverstaendnis_PM25_Beijing.ipynb` – explorative Datenanalyse (EDA).
- `02_Datenaufbereitung_Beijing.ipynb` – Datenbereinigung und -aufbereitung.
- `03_TFT_trainieren_inkl_Optuna.ipynb` (+ `_v3`) – TFT-Training inkl. Hyperparameter-Tuning mit Optuna.
- `04_TFT_Modelle_vergleichen.ipynb` – Vergleich der trainierten TFT-Modelle.
- `05_Modellvergleich_all.ipynb` – Gesamtvergleich Prophet vs. Chronos vs. TFT.
- `06_Prophet_Konfidenzintervalle.ipynb` – Prophet-Prognosen mit Konfidenzintervallen.
- `lightning_logs/` – Trainingsprotokolle von PyTorch Lightning (automatisch erzeugt).

### `data/`
- `PRSA_Data_20130301-20170228/` – Rohdaten der zwölf Beijing-Messstationen (2013–2017).
- `prepared/` – für Prophet aufbereitete Trainings-/Testdaten (`basis/`, `behandelt/`).
- `prepared_chronos/` – dieselben Daten im Chronos-Format (`basis/`, `behandelt/`).
- `ergebnis_*.csv` – Ergebnis-Tabellen der Modellläufe (Metriken, Benchmarks, Ablationen).

### `dashboard/`
- `PM25_Dashboard.html` – das fertige interaktive Dashboard.
- `build_dashboard.py` – erzeugt das Dashboard aus den Ergebnisdaten.
- Für die Veröffentlichung wird `PM25_Dashboard.html` als `docs/index.html` ins Wurzelverzeichnis kopiert (GitHub Pages).

### `notebooks_artefakte/`
Archiv älterer Notebook-Fassungen (`*.BACKUP*`, frühere Nummerierungen, `SpaeterLoeschen_*`).
Dient nur der Nachvollziehbarkeit – für aktuelle Arbeit `notebooks_fv/` verwenden.

## Umgebung einrichten (`ts-tutorial.yml`)

Die Conda-Umgebung enthält Prophet, Chronos und PatchTST (über HuggingFace `transformers`, plus `datasets` und `gluonts`).

```bash
conda env update -f ts-tutorial.yml --prune
conda activate ts-tutorial
```

> **⚠️ Nur unter Windows lauffähig.** Die `ts-tutorial.yml` wurde unter Windows exportiert und enthält Windows-spezifische Conda-Builds (`win-64`, `mingw`, `vs2015_runtime` u. a.). Unter macOS/Linux schlägt `conda env update` deshalb fehl. Wer nicht auf Windows arbeitet, installiert die Kernpakete stattdessen manuell: `prophet`, `chronos-forecasting`, `transformers`, `datasets`, `gluonts`, `torch`, `pandas`, `matplotlib`, `jupyterlab`.
>
> **Hinweis zur Kodierung:** Die Datei ist als **UTF-8** gespeichert. Beim Neu-Exportieren unter PowerShell bitte `conda env export | Out-File -Encoding utf8 ts-tutorial.yml` verwenden — sonst entsteht UTF-16, das der conda-Parser mit dem Fehler `unacceptable character #x0000` ablehnt.
</content>
