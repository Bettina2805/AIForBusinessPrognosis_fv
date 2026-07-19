<div align="center">

# 🔮 Business-Prognosis

### Zeitreihen-Prognose mit Prophet

<img src="images/prophet_wizard.png" alt="Prophet – Time Series Forecasting" width="420" />

<br/>

![Hochschule Aalen](https://img.shields.io/badge/Hochschule%20Aalen-SS%202026-8A2BE2)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Prophet](https://img.shields.io/badge/Forecasting-Prophet-4B0082)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)

*Studienprojekt an der Hochschule Aalen, Sommersemester 2026*

</div>

---

## 📌 Über das Projekt

Ziel des Projekts ist es, das Forecasting-Verfahren **Prophet** am Beispiel realer
Verkaufszahlen (Rossmann-Filialen) praktisch zu erproben und für andere Studierende
aufzubereiten – als **Präsentation**, **Demo** und **Tutorial**.

Prophet (Facebook/Meta) ist ein additives Modell aus **Trend**, **Saisonalität** und
**Feiertagen**. Der Reiz: Es ist robust, interpretierbar und lässt sich vom Analysten
gezielt mit Domänenwissen verbessern.

---

## 📈 Prophet-Tutorial: „Analyst-in-the-Loop"

Am Beispiel der **Rossmann-Filiale 1097 (Kölner Hauptbahnhof)** wird Schritt für Schritt
vom einfachen Baseline-Modell zu einer optimierten Vorhersage gearbeitet.
Das vollständige Demo-Notebook ist
[`1_prophet_demo_final.ipynb`](notebooks/1_prophet_demo_final.ipynb):

| Schritt | Modell | Erweiterung |
|:---:|:---|:---|
| 1 | Baseline | Trend + Saisonalität |
| 2 | + Feiertage | bundesweite deutsche Feiertage |
| 3 | + Regionales | NRW-Feiertage + Karneval |
| 4 | + Zeitfenster | Wirkungsfenster rund um Feiertage |
| 5 | + Regressor | Promotionen als zusätzliche Einflussgröße |

> 🦢 **Black-Swan-Stresstest:** Ein Zusatzkapitel zeigt, wo Prophet an Grenzen stößt,
> wenn die gelernte Saisonalität auf einen plötzlichen Strukturbruch in den Daten trifft.

---

## 🎓 Hands-On für Studierende

Das Notebook [`2_prophet_handson_students.ipynb`](notebooks/2_prophet_handson_students.ipynb)
ist ein **Crashkurs zum Selbermachen**. Anhand eines Beispiel-Datensatzes (Verkäufe der
„SkyDrive X1 Pro" SSD) lösen die Studierenden zwei Aufgaben:

1. **Aufgabe 1** – ein erstes Prophet-Modell *ohne* Feiertage trainieren („naives Modell")
2. **Aufgabe 2** – das Modell um den **Black Friday** als Feiertag erweitern („Experten-Modell")

Setup, Datengenerierung und Visualisierungen sind vorgegeben (einfach ausführen), sodass
der Fokus auf dem Modellieren liegt. Ein direkter Vergleich (naiv vs. Experte) und
Diskussionsfragen runden die Übung ab. Die vollständige Musterlösung liegt in
[`3_prophet_handson_solution.ipynb`](notebooks/3_prophet_handson_solution.ipynb).

---

## 🗂️ Projektstruktur

```
.
├── data/
│   ├── rossmann-store-sales/   # Rossmann-Datensatz (train, test, store, …)
│   └── flights.csv             # Flugdaten für den Black-Swan-Stresstest
├── notebooks/
│   ├── 1_prophet_demo_final.ipynb         # vollständige Demo (Rossmann)
│   ├── 2_prophet_handson_students.ipynb   # Übung für Studierende
│   ├── 3_prophet_handson_solution.ipynb   # Musterlösung
│   ├── cross_validation.PNG               # Abbildung zur Demo
│   └── umsaetzeRossmannFiliale_v2.png     # Abbildung zur Demo
├── powerpoint/
│   └── Prophet_Einstiegspräsentation.pptx
├── literature/                 # Wissenschaftliche Quellen (PDFs)
├── images/                     # Key Visuals (README-Bilder)
├── ts-tutorial.yml             # Conda-Umgebung
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

Die benötigte Umgebung lässt sich mit Conda erstellen:

```bash
conda env create -f ts-tutorial.yml --no-channel-priority
conda activate ts-tutorial
jupyter lab
```

**Wichtigste Pakete:** Python 3.10 · Prophet · Pandas · NumPy · Matplotlib · PyTorch · JupyterLab

---

## 📊 Daten

- **Rossmann Store Sales** – tägliche Umsätze einzelner Filialen (Kaggle-Datensatz)
- **Flugdaten** – ergänzender Datensatz für den Strukturbruch-/Black-Swan-Stresstest

---

## 📚 Literatur

Im Ordner `literature/` liegen die zugrundeliegenden Paper:

**Taylor, S. J. & Letham, B. (2018). *Forecasting at Scale.* The American Statistician 72(1), 37–45.**
Das Original-Prophet-Paper von Meta. Es führt das additive Modell aus Trend, Saisonalität und Feiertagen ein, das auch von Analysten ohne Zeitreihen-Expertise bedient werden kann – die Grundlage dieses Projekts.

**Jung, S. et al. (2020). *A Worrying Analysis of Probabilistic Time-series Models for Sales Forecasting.***
Die Autoren vergleichen drei prominente probabilistische Zeitreihenmodelle unter streng standardisierten Bedingungen (großer Datensatz, einheitliche Cross-Validation und Hyperparameter-Wahl). Ergebnis: Einfache Baselines wie Lineare Regression und ein Multilayer-Perceptron schlagen die komplexen Modelle bei Punktmetriken (RMSE, MAPE) – ein Warnsignal gegen blindes Vertrauen in aufwendige Verfahren.

**Žunić, E. et al. (2020). *Application of Facebook's Prophet Algorithm for Successful Sales Forecasting.***
Vorgestellt wird ein Framework, das mit Prophet und einer Backtesting-Strategie produktgenaue Verkaufsprognosen erstellt und das Sortiment nach erwarteter Prognose-Zuverlässigkeit klassifiziert. Getestet wird es an realen Verkaufsdaten eines der größten Handelsunternehmen Bosnien-Herzegowinas, also unter echten, volatilen Praxisbedingungen.

**Triebe, O. et al. (2021). *NeuralProphet – Explainable Forecasting at Scale.***
Das Paper stellt NeuralProphet vor, einen PyTorch-basierten Nachfolger von Prophet, der dessen interpretierbare Komponenten beibehält, aber um lokalen Kontext (Autoregression, Kovariaten) erweitert. In den Experimenten verbessert NeuralProphet die Kurz- bis Mittelfristprognose gegenüber Prophet um 55–92 %.

**Blume, T. (2023). *Fixing Prophet's Forecasting Issue* (Towards Data Science).**
Praxisnaher Blog-Artikel, der Prophets bekanntes Genauigkeitsproblem auf seinen flexiblen Trend zurückführt: Changepoints können den Trend ins Extreme extrapolieren („insane trend") und nützliches Signal aus den Residuen verschlucken. Anhand offener Datensätze zeigt der Autor, wie man den Trend gezielt einschränkt, um die Prognosegüte zu verbessern.

**Shapiro, S. & Panvelwala, B. (2026). *Prophet as a Reproducible Forecasting Framework.***
Die Studie betrachtet Prophet nicht als neuen Algorithmus, sondern als Werkzeug für reproduzierbare Forecasting-Workflows in Business und Finance und vergleicht es kontrolliert mit ARIMA-Varianten und Random Forest. Sie betont Prophets additive, interpretierbare Struktur und den standardisierten, gut dokumentierbaren Ablauf als Vorteil für Nachvollziehbarkeit und Auditierbarkeit.

---

<div align="center">

## 👥 Team

<img src="images/prophet_team.png" alt="Prophet – Business Forecasting Team" width="300" />

<br/>

**Bettina & Kai** — Hochschule Aalen · SS 2026

</div>
