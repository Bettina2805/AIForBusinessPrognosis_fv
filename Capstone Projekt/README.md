<div align="center">

# Capstone Projekt

### Business-Prognosis – Hochschule Aalen, SS 2026

![Hochschule Aalen](https://img.shields.io/badge/Hochschule%20Aalen-SS%202026-8A2BE2)

</div>

---

Dieser Ordner enthält das **Capstone-Projekt** zum Kurs Business-Prognosis.

## Umgebung einrichten (`ts-tutorial.yml`)

Die Conda-Umgebung enthält Prophet, Chronos und PatchTST (über HuggingFace `transformers`, plus `datasets` und `gluonts`).

```bash
conda env update -f ts-tutorial.yml --prune
conda activate ts-tutorial
```

> **⚠️ Nur unter Windows lauffähig.** Die `ts-tutorial.yml` wurde unter Windows exportiert und enthält Windows-spezifische Conda-Builds (`win-64`, `mingw`, `vs2015_runtime` u. a.). Unter macOS/Linux schlägt `conda env update` deshalb fehl. Wer nicht auf Windows arbeitet, installiert die Kernpakete stattdessen manuell: `prophet`, `chronos-forecasting`, `transformers`, `datasets`, `gluonts`, `torch`, `pandas`, `matplotlib`, `jupyterlab`.
>
> **Hinweis zur Kodierung:** Die Datei ist als **UTF-8** gespeichert. Beim Neu-Exportieren unter PowerShell bitte `conda env export | Out-File -Encoding utf8 ts-tutorial.yml` verwenden — sonst entsteht UTF-16, das der conda-Parser mit dem Fehler `unacceptable character #x0000` ablehnt.
