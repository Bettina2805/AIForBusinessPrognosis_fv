<div align="center">

# 🔮 Business-Prognosis · Chronos

### Zeitreihen-Prognose mit Chronos (Foundation Model)

<img src="images/Chronos.png" alt="Chronos – Time Series Forecasting" width="420" />

<br/>

![Hochschule Aalen](https://img.shields.io/badge/Hochschule%20Aalen-SS%202026-8A2BE2)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Chronos](https://img.shields.io/badge/Forecasting-Chronos-FF9900)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)

*Studienprojekt an der Hochschule Aalen, Sommersemester 2026*

</div>

---

## 📌 Über das Projekt

Dieses Teilprojekt überträgt das **Prophet**-Material auf **Chronos** – ein
**vortrainiertes Foundation Model** für Zeitreihen (Amazon Science). Wie beim
Prophet-Teil entstehen **Präsentation**, **Demo** und **Tutorial**.

Der spannende Kontrast: Prophet ist „Analyst-in-the-Loop" (du baust Feiertage,
Regressoren etc. selbst ein), Chronos sagt **zero-shot** vorher – ganz **ohne Training
und ohne Feature-Engineering**. Beides wird auf **denselben Rossmann-Daten** gezeigt, um
direkt vergleichen zu können.

---

## 📈 Demo: dieselben Daten wie Prophet

Am Beispiel der **Rossmann-Filiale 1097** wird vom naiven Zero-Shot-Forecast zu einer
optimierten Vorhersage gearbeitet – Notebook
[`1_chronos_demo.ipynb`](notebooks/1_chronos_demo.ipynb):

| Kapitel | Inhalt | Prophet-Gegenstück |
|:---:|:---|:---|
| 1 | Daten & Vorbereitung (Rossmann) | Datenexploration |
| 2 | Zero-Shot vs. einfacher Prophet | Baseline (Trend+Saison) |
| 3 | Schließtage maskieren (NaN vs. Nullen) | + Feiertage |
| 4 | Stellschrauben: Kontext, Horizont, Modellgröße | + regionale Feiertage/Zeitfenster |
| 5 | Chronos-2: Kovariate & Panel | + Regressor / alle Filialen |
| 6 | Grenzen: Black-Swan-Stresstest (Flugdaten) | Unsicherheit / Strukturbruch |

> 🦢 **Black-Swan-Stresstest** in Kapitel 6 mit `data/flights.csv` – dieselben Flugdaten
> wie beim Prophet-Teil (Corona-Einbruch Anfang 2020).

---

## 🎓 Hands-On für Studierende

[`2_chronos_handson_students.ipynb`](notebooks/2_chronos_handson_students.ipynb) –
Crashkurs zum Selbermachen mit dem synthetischen **„SkyDrive X1 Pro"**-Datensatz
(Trend + Wochenmuster + Black-Friday-Peak):

| Aufgabe | Thema | Zeit |
|:---:|:---|:---:|
| 1 | Naiver Zero-Shot-Forecast mit Chronos-Bolt | ~4 min |
| 2 | Black Friday als Kovariate (Chronos-2) | ~5 min |
| 3 | Drei Filialen in **einem** Aufruf (Panel) | ~5 min |

Musterlösung in
[`3_chronos_handson_solution.ipynb`](notebooks/3_chronos_handson_solution.ipynb).

### Bonus

[`Airpassengers.ipynb`](notebooks/Airpassengers.ipynb) – interaktive Demo zur **Wirkung
der Kontextfenster-Länge** am Klassiker **AirPassengers** (Daten werden per URL geladen,
keine lokale CSV nötig).

---

## 🗂️ Projektstruktur

```
chronos/
├── README.md
├── ts-tutorial.yml                      # Conda-Umgebung (+ Chronos)
├── data/
│   ├── rossmann-store-sales/            # Rossmann-Datensatz (identisch zum Prophet-Teil)
│   │   ├── train.csv                    # Tagesumsätze aller Filialen (2013–2015)
│   │   ├── test.csv                     # Testzeitraum ohne Sales-Spalte
│   │   ├── store.csv                    # Filial-Metadaten (Typ, Sortiment, …)
│   │   └── sample_submission.csv        # Kaggle-Vorlage (nicht für Notebooks nötig)
│   └── flights.csv                      # Flugdaten für den Black-Swan-Stresstest (Kap. 6)
├── images/
│   ├── Chronos.png                      # Key Visual (README, Präsentation)
│   └── Cronos_ppt.png
├── literature/                          # Chronos-Paper & weiterführende Quellen (PDF)
│   ├── 4__Ansari_et al_2024_Chronos_Learning the Language of Time Series.pdf
│   ├── AnsariEtAl_Chronos2.pdf
│   ├── VergleichbareArbeitenZuChronos.pdf
│   ├── energies-19-00362.pdf
│   └── 10.1016_j.ijepes.2026.111792.pdf
├── notebooks/
│   ├── 1_chronos_demo.ipynb             # Demo (Rossmann + Flugdaten)
│   ├── 2_chronos_handson_students.ipynb # Übung für Studierende
│   ├── 3_chronos_handson_solution.ipynb # Musterlösung
│   └── Airpassengers.ipynb              # Bonus: Kontextfenster interaktiv
└── presentation/
    └── Chronos_Praesentation.pptx       # Einstiegspräsentation
```

---

## ⚙️ Setup

Chronos baut auf der bestehenden Prophet-Umgebung (`ts-tutorial`) auf und ergänzt nur
die Chronos-Pakete. **Empfohlen:** in die vorhandene Env installieren –

```bash
conda activate ts-tutorial
pip install chronos-forecasting scikit-learn "pandas[pyarrow]"
```

`pip install chronos-forecasting` zieht `transformers`, `accelerate` und `einops`
automatisch mit; `pandas[pyarrow]` wird nur für den optionalen Chronos-2-Teil gebraucht.

Alternativ lässt sich die Umgebung komplett aus der mitgelieferten Datei nachbauen
(sie enthält Prophet **und** Chronos):

```bash
conda env create -f ts-tutorial.yml --no-channel-priority
conda activate ts-tutorial
jupyter lab
```

**Wichtigste Pakete:** Python 3.10 · chronos-forecasting · PyTorch (CPU) · Pandas ·
NumPy · Matplotlib · JupyterLab

> Beim ersten `from_pretrained(...)` lädt das Modell automatisch von Hugging Face
> (einmalig Internet nötig, danach im Cache). Die empfohlenen **Bolt-small/base**-Modelle
> laufen auf der **CPU** in Sekunden.

---

## 📊 Daten

### Rossmann Store Sales (`data/rossmann-store-sales/`)

[Kaggle-Wettbewerb](https://www.kaggle.com/c/rossmann-store-sales) – tägliche Umsätze von
1.115 Drogerie-Filialen, **2013–2015**. Wird in der Demo und zum Vergleich mit Prophet
genutzt.

| Datei | Inhalt | Spalten (Auszug) |
|:---|:---|:---|
| `train.csv` | Historie inkl. Umsatz | Store, Date, Sales, Customers, Open, Promo, StateHoliday, SchoolHoliday |
| `test.csv` | Testzeitraum ohne Zielvariable | wie train, ohne `Sales` |
| `store.csv` | Filial-Stammdaten | Store, StoreType, Assortment, CompetitionDistance, … |
| `sample_submission.csv` | Kaggle-Abgabeformat | Id, Sales |

### Flugdaten (`data/flights.csv`)

Europäische Flugverkehrszahlen (identisch zum Prophet-Teil) für den
**Black-Swan-/Corona-Stresstest** in Kapitel 6 der Demo. Relevante Spalten:
`FLT_DATE` (Datum), `FLT_TOT_1` (Flüge gesamt pro Flughafen und Tag).

### Hands-On & Bonus

- **SkyDrive X1 Pro** – synthetische Zeitreihe, wird direkt im Hands-On-Notebook erzeugt
  (keine externe Datei).
- **AirPassengers** – wird in `Airpassengers.ipynb` von GitHub geladen.

---

## 📚 Literatur

Im Ordner `literature/` liegen die zentralen Paper und ergänzende Quellen:

| Datei | Thema |
|:---|:---|
| `4__Ansari_et al_2024_Chronos_Learning the Language of Time Series.pdf` | Chronos (Foundation Model) |
| `AnsariEtAl_Chronos2.pdf` | Chronos-2 (Kovariaten & Panel) |
| `VergleichbareArbeitenZuChronos.pdf` | Überblick verwandter Arbeiten |
| `energies-19-00362.pdf` | Anwendungs-/Domänenbezug |
| `10.1016_j.ijepes.2026.111792.pdf` | Weiterführende Forschung |

**Primärquellen (Online):**

- **Ansari, A. F. et al. (2024). *Chronos: Learning the Language of Time Series.*** TMLR.
  [arXiv:2403.07815](https://arxiv.org/abs/2403.07815)
- **Ansari, A. F. et al. (2025). *Chronos-2: From Univariate to Universal Forecasting.***
  [arXiv:2510.15821](https://arxiv.org/abs/2510.15821)

---

<div align="center">

**Bettina & Kai** — Hochschule Aalen · SS 2026

</div>
