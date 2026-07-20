# Storyline — PM2.5-Prognose Beijing: Klassik vs. Foundation-Modell vs. Deep Learning

**Roter Faden:** *„Wir vergleichen vier grundverschiedene Prognose-Philosophien fair auf denselben
Daten — und die Antwort, welches Modell gewinnt, ist überraschend nuanciert."*

Reihenfolge der Modelle durchgängig: **Seasonal-Naive → Prophet → Chronos-2 → TFT**
(einfach → komplex). Metrik: **MASE** (< 1 = besser als die Naive-Baseline).

---

## Teil 1 — Problem & Aufgabe (2–3 Folien)

**Folie 1 — Hook: Warum PM2.5 Beijing?**
Kernaussage: Feinstaub ist ein akutes Gesundheitsrisiko; verlässliche Kurzfrist-Prognosen (8–72 h)
stützen Warnungen und Planung. Bild `images/peopleinbejing2013.jpeg`, ein, zwei Health-Fakten.

**Folie 2 — Datensatz & Ziel.**
Kernaussage: 12 Messstationen, stündlich, 2013-03 bis 2017-02; Wetter + Co-Schadstoffe als
Kovariaten. Ziel: PM2.5 mehrere Stunden voraus. Karte/Stationsliste (`data/stations_geo.csv`).

**Folie 3 — Die Leitfrage.**
Kernaussage: „Schlägt ein modernes Modell die simple Baseline — und lohnt sich der Aufwand von
Deep Learning gegenüber klassischer Statistik oder einem trainingsfreien Foundation-Modell?"

---

## Teil 2 — Methodik & die vier Ansätze (4–5 Folien)

**Folie 4 — Fairer Testaufbau.**
Kernaussage: Training bis 30.08.2016, **Rolling-Window-Backtest** 09/2016–02/2017 (Versatz 15 Tage,
12 Folds), Horizonte 8/24/48/72 h, alle Modelle auf identischen Fenstern. Metrik MASE erklären
(1.0 = Naive-Niveau).

**Folie 5 — Die vier Philosophien (Übersichtstabelle).**
Kernaussage: Vier grundverschiedene Ansätze — genau das macht den Vergleich spannend.
Nutze die Tabelle aus Notebook 05, Abschnitt 7b:

| | Seasonal Naive | Prophet | Chronos-2 | TFT |
|---|---|---|---|---|
| Typ | Baseline (Vorjahreswert) | klassisch-statistisch, additiv | Transformer-Foundation-Modell | tiefes neuronales Netz |
| Training | keins | pro Fenster neu gefittet | zero-shot (kein Training) | einmal global trainiert, eingefroren |
| Stärke | robuster Referenzwert | interpretierbar | starke Muster ohne Training | komplexe, nichtlineare Zusammenhänge |
| Schwäche | ignoriert aktuelle Lage | lineare Regressoren | Blackbox | Trainingsaufwand, Blackbox |

**Folie 6 — Annahmen & Fairness (Vertrauens-Folie).**
Kernaussage: Wir legen die Spielregeln offen. Drei Punkte:
- *Perfect-Prognosis* = optimistische Obergrenze (Wetter „bekannt"); zusätzlich Persistenz-Variante.
- TFT auf 30.08.2016 eingefroren, Prophet/Chronos nutzen pro Fold aktuellere Historie.
- Test ist **out-of-time**, nicht out-of-station (alle 12 waren im TFT-Training).

---

## Teil 3 — Ergebnisse (Herzstück, 4–5 Folien)

**Folie 7 — Hauptergebnis: MASE/MAE je Horizont.**
Kernaussage: **Chronos-2 und TFT gleichauf an der Spitze, beide deutlich vor Prophet und Naive.**
Grafik `grafiken/vergleich_rolling_notebook.png`. Zahlen (Mittel über alle 12 Stationen):

| Horizont | Naive | Prophet (Pers.) | Prophet (PP) | Chronos-2 | TFT |
|---|---|---|---|---|---|
| 8 h  | 1,44 | 0,81 | 0,77 | **0,37** | 0,41 |
| 24 h | 1,24 | 0,97 | 0,74 | 0,42 | **0,42** |
| 48 h | 1,17 | 1,27 | 0,84 | **0,55** | 0,55 |
| 72 h | 1,31 | 1,48 | 0,98 | 0,68 | **0,65** |

**Folie 8 — Ist der Unterschied echt? (Signifikanz).**
Kernaussage: **TFT vs. Chronos-2 statistisch gleichauf** (kein belastbarer Unterschied); beide
schlagen Prophet signifikant. Grafik `grafiken/signifikanz_tft_vs_chronos.png` (gepaarte
MASE-Differenzen um 0) + Wilcoxon-Ergebnisse aus Abschnitt 10. → *„TFT ist NICHT ‚das beste'
Modell — Chronos zieht ohne jedes Training gleich."*

**Folie 9 — Interpretierbarkeit als Prophet-Stärke.**
Kernaussage: Prophet ist schwächer in der Genauigkeit, aber **erklärt seine Vorhersage**.
Grafik `grafiken/prophet_komponenten_Dongsi.png` — Heizperiode im Jahresgang, Abend-Peak im
Tagesgang, Feiertags-Ausschläge. Trade-off: Interpretierbarkeit ↔ Genauigkeit.

**Folie 10 — Der ehrliche Befund: das Frühlingsfest.**
Kernaussage: **Kein Modell beherrscht den Neujahrs-Peak.** Warum: Feuerwerk/Verhalten treiben das
Extrem — dieser Treiber steckt in keiner Kovariate; ein seltenes, bewegliches, kurzes Ereignis
kann keines der Modelle nachbilden. Beispiel-Fold über den Jahreswechsel im Kurven-Viewer zeigen.

**Folie 11 — Zwei Vertiefungen.**
Kernaussage: (a) *Optimismus-Band*: Prophet (PP) vs. (Pers.) zeigt den „Preis, das Wetter nicht zu
kennen" (72 h: 0,98 → 1,48). (b) *Stationstyp-Effekt*: Prophet holt an ruhigen Vorstadt-/
Hintergrund-Stationen auf (MASE 0,73) gegenüber Urban (0,89), bleibt aber hinter Chronos/TFT.

---

## Teil 4 — Einordnung, Demo, Fazit (3 Folien)

**Folie 12 — „Welches Modell wann?" (Empfehlung).**
- **Chronos-2** — beste Genauigkeit *ohne* Training; ideal, wenn schnell einsatzbereit.
- **TFT** — gleich gut, aber einmal trainieren, dann billig & skalierbar über viele Stationen.
- **Prophet** — wenn Interpretierbarkeit / Erklärbarkeit zählt.
- **Seasonal Naive** — Sanity-Floor, den jedes Modell schlagen muss.

**Folie 13 — Live-Demo: interaktives Dashboard.**
Kernaussage: Alle Ergebnisse interaktiv. Klick-Pfad: (1) Fehlervergleich mit Metrik-Umschaltung,
(2) eine Station mit klarem TFT/Chronos-Vorsprung im Kurven-Viewer, (3) Beispiel-Fold über
Neujahr (alle scheitern), (4) Prophet PP vs. Pers. für das Optimismus-Band. Datei
`dashboard/PM25_Dashboard.html`.

**Folie 14 — Fazit & Limitierungen.**
Kernaussage: Moderne Modelle schlagen die Baseline klar; Foundation-Modell (Chronos) und Deep
Learning (TFT) gleichauf; klassische Statistik (Prophet) bleibt interpretierbar, aber genauer nur
im Mittelfeld. Limitierungen: Perfect-Prognosis-Obergrenze, out-of-time-Test, Extremereignisse
(Neujahr) ungelöst.

---

## Optionaler Ausblick — zusätzliche Kovariaten (Wind, Geo, Co-Schadstoffe)

Deine Ablation (`ergebnis_ablation_leicht_aggregiert.csv`) zeigt ein differenziertes Bild:
**Wind hilft, reine Geo-Koordinaten nicht.**

| Variante | MAE | RMSE |
|---|---|---|
| Basis | 19,40 | 37,75 |
| + Windgeschw. | 18,53 | 34,24 |
| + Windrichtung | 18,48 | 35,73 |
| + beide Wind | 18,55 | **32,93** |
| + beide Wind + Geo | 18,92 | 33,88 |

Aussage fürs Deck: „Wind als physikalisch sinnvolle Kovariate verbessert TFT **leicht**;
zusätzliche **Geo-Koordinaten bringen keinen Nutzen** (eher minimal schlechter)." Das ist sogar die
*stärkere* Story als „alles hilft" — es zeigt, dass man Kovariaten begründet auswählen muss.

> ⚠️ **Vorsicht:** Effekte sind klein und beruhen auf nur 2 Seeds (Basis 19,40 ± 1,30 streut fast so
> stark wie die Verbesserung) — Richtung konsistent, aber als „leichte Verbesserung durch Wind"
> formulieren, nicht als harten Beweis. Zudem stammen diese Zahlen aus einem *anderen*
> Auswertungssetup als der Hauptvergleich (Folie 7) — als separates Experiment kennzeichnen.

Ergänzend: Co-Schadstoffe (`ergebnis_coschadstoffe_*`) und Lag-Wetter (`ergebnis_tft_lag_*`) als
weitere Kovariaten-Experimente verfügbar, falls du das Thema vertiefen willst.

---

## Muss noch etwas laufen?

**Für die Kern-Story: nein.** Hauptvergleich (alle 12 Stationen), Signifikanz (Abschnitt 10),
Prophet-Komponenten (Abschnitt 11) und Dashboard sind fertig und gespeichert.

**Optional**, falls gewünscht:
- Wind/Geo-TFT auf identischer Rolling-Methodik (nur nötig, wenn die Ausblicks-Zahl direkt
  vergleichbar sein soll).
- Feinschliff der Folien-Grafiken (Beschriftung/Helligkeit fürs Beamer-Format).
