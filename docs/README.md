# PM2.5 Beijing – Modellvergleich Dashboard (GitHub Pages)

Dieser Ordner veröffentlicht das Dashboard als Webseite über **GitHub Pages**.

- `index.html` – das komplette Dashboard (eigenständig, keine externen Abhängigkeiten).
- `.nojekyll` – schaltet die Jekyll-Verarbeitung ab, damit die Datei 1:1 ausgeliefert wird.

## Aktivieren (einmalig)

1. Diesen Ordner committen und pushen:
   ```bash
   git add docs
   git commit -m "Dashboard fuer GitHub Pages"
   git push
   ```
2. Auf GitHub: **Settings → Pages**
   - Source: *Deploy from a branch*
   - Branch: `main`, Ordner: `/docs` → **Save**
3. Nach ~1 Minute erscheint oben die URL, z. B.
   `https://<dein-name>.github.io/<repo>/`

Diese URL kann jeder öffnen – kein Login, keine Installation.

## Aktualisieren

Wenn das Dashboard neu gebaut wurde (`dashboard/build_dashboard.py`), die neue
`PM25_Dashboard.html` einfach wieder als `docs/index.html` kopieren, committen, pushen.

> **Wichtig:** Der Ordner `docs/` muss im **Wurzelverzeichnis des Repos** liegen,
> damit GitHub Pages die Option `/docs` anbietet. Liegt dein Repo-Root eine Ebene
> höher, verschiebe diesen `docs/`-Ordner dorthin.
