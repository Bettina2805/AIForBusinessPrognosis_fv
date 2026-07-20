#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut ein eigenstaendiges, offline lauffaehiges HTML-Dashboard fuer den PM2.5-Modellvergleich.

Liest:
  ../data/ergebnis_modellvergleich_rolling.csv   (Metriken je Fold/Station/Horizont/Modell)
  ../data/vorhersagen_rolling.csv                (Prognosekurven; optional -- Kurven-Tab)

Schreibt:
  PM25_Dashboard.html  (Daten eingebettet, keine externen Bibliotheken/CDN noetig)

Aufruf (in einer Umgebung mit pandas, z. B. chronos_env):
  python build_dashboard.py
"""
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

HIER = Path(__file__).resolve().parent
DATA = HIER.parent / "data"
METRIK_CSV = DATA / "ergebnis_modellvergleich_rolling.csv"
KURVEN_CSV = DATA / "vorhersagen_rolling.csv"
OUT_HTML = HIER / "PM25_Dashboard.html"

FARBEN = {
    "Seasonal Naive": "#E0912F",
    "Prophet (Pers.)": "#7FB3FF",
    "Prophet (PP)": "#1f6feb",
    "Chronos-2": "#7B2CBF",
    "TFT": "#2C5F2D",
}
MODELL_REIHENFOLGE = ["Seasonal Naive", "Prophet (Pers.)", "Prophet (PP)", "Chronos-2", "TFT"]

# Kurven-Spalten -> Modellname
KURVEN_MAP = {
    "yhat_chronos": "Chronos-2",
    "yhat_tft": "TFT",
    "yhat_prophet_pp": "Prophet (PP)",
    "yhat_prophet_pers": "Prophet (Pers.)",
    "yhat_naive": "Seasonal Naive",
}


def horizont_zu_int(x):
    return int(str(x).replace("h", "").strip())


def lade_metriken():
    if not METRIK_CSV.exists():
        sys.exit(f"FEHLER: {METRIK_CSV} nicht gefunden. Erst Notebook 05 (Abschnitt 9b) laufen lassen.")
    d = pd.read_csv(METRIK_CSV)
    d["Horizont"] = d["Horizont"].map(horizont_zu_int)
    d = d.rename(columns={"MAPE %": "MAPE"})
    zeilen = []
    for _, r in d.iterrows():
        zeilen.append({
            "Fold": str(r["Fold"]), "Station": str(r["Station"]),
            "Horizont": int(r["Horizont"]), "Modell": str(r["Modell"]),
            "MAE": round(float(r["MAE"]), 2), "RMSE": round(float(r["RMSE"]), 2),
            "MASE": round(float(r["MASE"]), 3), "MAPE": round(float(r["MAPE"]), 1),
        })
    return d, zeilen


def lade_kurven():
    if not KURVEN_CSV.exists():
        return {}
    d = pd.read_csv(KURVEN_CSV, parse_dates=["ds"])
    d = d.sort_values(["Fold", "Station", "ds"]).reset_index(drop=True)
    kurven = {}
    for (fold, station), g in d.groupby(["Fold", "Station"]):
        key = f"{fold}|{station}"
        series = {}
        for spalte, modell in KURVEN_MAP.items():
            if spalte in g.columns:
                series[modell] = [round(float(v), 1) for v in g[spalte].tolist()]
        kurven[key] = {
            "ds": [pd.Timestamp(t).strftime("%Y-%m-%d %H:%M") for t in g["ds"]],
            "lead": [int(v) for v in g["lead"].tolist()],
            "y": [round(float(v), 1) for v in g["y"].tolist()],
            "series": series,
        }
    return kurven


def main():
    df, metriken = lade_metriken()
    kurven = lade_kurven()

    stationen = sorted(df["Station"].unique().tolist())
    folds = sorted(df["Fold"].astype(str).unique().tolist())
    horizonte = sorted(df["Horizont"].unique().tolist())
    modelle = [m for m in MODELL_REIHENFOLGE if m in df["Modell"].unique().tolist()]
    modelle += [m for m in df["Modell"].unique().tolist() if m not in modelle]

    data = {
        "meta": {
            "stationen": stationen, "folds": folds, "horizonte": horizonte,
            "modelle": modelle, "farben": FARBEN,
            "n_folds": len(folds), "hat_kurven": bool(kurven),
        },
        "metriken": metriken,
        "kurven": kurven,
    }

    js_data = json.dumps(data, ensure_ascii=False)
    html = HTML_TEMPLATE.replace("/*__DATA__*/", js_data)
    html = html.replace("__GENERATED__", datetime.now().strftime("%d.%m.%Y %H:%M"))
    html = html.replace("__NFOLDS__", str(len(folds)))
    html = html.replace("__STATIONEN__", ", ".join(stationen))
    OUT_HTML.write_text(html, encoding="utf-8")
    groesse = OUT_HTML.stat().st_size / 1024
    print(f"Dashboard geschrieben: {OUT_HTML}  ({groesse:.0f} KB)")
    print(f"  Metrik-Zeilen: {len(metriken)} | Kurven: {'ja ('+str(len(kurven))+' Fenster)' if kurven else 'nein -- Abschnitt 9d im Notebook noch laufen lassen'}")
    print("  Zum Anzeigen einfach die HTML-Datei im Browser oeffnen (Doppelklick).")


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PM2.5 Beijing - Modellvergleich Dashboard</title>
<style>
  :root{
    --bg:#0f1420; --panel:#161d2e; --panel2:#1d263b; --ink:#e8ecf4; --muted:#9aa7bd;
    --line:#2a3348; --accent:#4da3ff;
  }
  *{box-sizing:border-box}
  body{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
       background:var(--bg);color:var(--ink);font-size:15px}
  header{padding:18px 24px;border-bottom:1px solid var(--line);background:var(--panel)}
  header h1{margin:0;font-size:20px}
  header .sub{color:var(--muted);font-size:13px;margin-top:4px}
  .tabs{display:flex;gap:4px;padding:12px 24px 0;background:var(--panel);border-bottom:1px solid var(--line)}
  .tab{padding:9px 16px;border:1px solid var(--line);border-bottom:none;border-radius:8px 8px 0 0;
       cursor:pointer;color:var(--muted);background:transparent}
  .tab.active{background:var(--bg);color:var(--ink);font-weight:600}
  main{padding:20px 24px;max-width:1180px;margin:0 auto}
  .panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin-bottom:18px}
  .controls{display:flex;flex-wrap:wrap;gap:18px;align-items:center;margin-bottom:8px}
  .ctl{display:flex;flex-direction:column;gap:6px}
  .ctl label{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
  select,button{background:var(--panel2);color:var(--ink);border:1px solid var(--line);
       border-radius:8px;padding:7px 10px;font-size:14px}
  .chips{display:flex;flex-wrap:wrap;gap:8px}
  .chip{display:inline-flex;align-items:center;gap:7px;padding:6px 11px;border:1px solid var(--line);
        border-radius:20px;cursor:pointer;user-select:none;background:var(--panel2);font-size:13px}
  .chip .dot{width:11px;height:11px;border-radius:50%}
  .chip.off{opacity:.38}
  .radio{display:inline-flex;gap:0;border:1px solid var(--line);border-radius:8px;overflow:hidden}
  .radio button{border:none;border-radius:0;border-right:1px solid var(--line);padding:7px 12px}
  .radio button:last-child{border-right:none}
  .radio button.active{background:var(--accent);color:#04101f;font-weight:600}
  .hint{color:var(--muted);font-size:13px;line-height:1.5}
  svg{width:100%;height:auto;display:block}
  .legend{display:flex;flex-wrap:wrap;gap:14px;margin-top:10px;font-size:13px}
  .legend .it{display:flex;align-items:center;gap:7px;color:var(--ink)}
  .legend .sw{width:16px;height:4px;border-radius:2px}
  table{border-collapse:collapse;width:100%;font-size:13px;margin-top:12px}
  th,td{border:1px solid var(--line);padding:6px 9px;text-align:right}
  th:first-child,td:first-child{text-align:left}
  th{color:var(--muted);font-weight:600;background:var(--panel2)}
  .tt{position:fixed;pointer-events:none;background:#0b0f18;border:1px solid var(--line);
      border-radius:8px;padding:8px 10px;font-size:12px;line-height:1.5;display:none;z-index:10;box-shadow:0 6px 20px rgba(0,0,0,.4)}
  .kpi{font-size:12px;color:var(--muted);margin-top:6px}
  .warn{background:#3a2a12;border:1px solid #7a5a20;color:#f0d9a8;padding:12px 14px;border-radius:10px}
  a{color:var(--accent)}
</style>
</head>
<body>
<header>
  <h1>PM2.5 Beijing &mdash; Modellvergleich (Rolling-Window)</h1>
  <div class="sub">Stationen: __STATIONEN__ &nbsp;&middot;&nbsp; __NFOLDS__ Folds &nbsp;&middot;&nbsp; Chronos-2 &middot; TFT &middot; Prophet (Perfect-Prognosis + Persistenz) &middot; Seasonal Naive &nbsp;&middot;&nbsp; erstellt __GENERATED__</div>
</header>
<div class="tabs" id="tabs">
  <div class="tab active" data-tab="fehler">Fehlervergleich</div>
  <div class="tab" data-tab="kurven">Prognosekurven</div>
  <div class="tab" data-tab="vert">MASE-Verteilung</div>
</div>
<main>
  <section id="tab-fehler">
    <div class="panel">
      <div class="controls">
        <div class="ctl"><label>Metrik</label>
          <div class="radio" id="f-metrik">
            <button data-v="MASE" class="active">MASE</button>
            <button data-v="MAE">MAE</button>
            <button data-v="RMSE">RMSE</button>
            <button data-v="MAPE">MAPE %</button>
          </div>
        </div>
        <div class="ctl"><label>Station</label>
          <select id="f-station"></select>
        </div>
        <div class="ctl" style="flex:1"><label>Modelle</label>
          <div class="chips" id="f-modelle"></div>
        </div>
      </div>
      <svg id="f-chart" viewBox="0 0 960 440" preserveAspectRatio="xMidYMid meet"></svg>
      <div class="hint" id="f-hint"></div>
      <table id="f-table"></table>
    </div>
  </section>

  <section id="tab-kurven" style="display:none">
    <div class="panel" id="kurven-panel">
      <div class="controls">
        <div class="ctl"><label>Station</label><select id="k-station"></select></div>
        <div class="ctl"><label>Fold (Startdatum)</label><select id="k-fold"></select></div>
        <div class="ctl"><label>Horizont</label>
          <div class="radio" id="k-hor">
            <button data-v="8">8 h</button><button data-v="24">24 h</button>
            <button data-v="48">48 h</button><button data-v="72" class="active">72 h</button>
          </div>
        </div>
        <div class="ctl" style="flex:1"><label>Modelle</label><div class="chips" id="k-modelle"></div></div>
      </div>
      <svg id="k-chart" viewBox="0 0 960 430" preserveAspectRatio="xMidYMid meet"></svg>
      <div class="legend" id="k-legend"></div>
      <div class="hint" id="k-hint"></div>
    </div>
  </section>

  <section id="tab-vert" style="display:none">
    <div class="panel">
      <div class="controls">
        <div class="ctl"><label>Horizont</label>
          <div class="radio" id="v-hor">
            <button data-v="8">8 h</button><button data-v="24">24 h</button>
            <button data-v="48">48 h</button><button data-v="72" class="active">72 h</button>
          </div>
        </div>
        <div class="ctl" style="flex:1"><label>Modelle</label><div class="chips" id="v-modelle"></div></div>
      </div>
      <svg id="v-chart" viewBox="0 0 960 420" preserveAspectRatio="xMidYMid meet"></svg>
      <div class="hint">Boxplot der MASE-Werte ueber alle Folds &amp; Stationen. Rote Linie = MASE 1.0 (Seasonal-Naive-Niveau). Box = 25.&ndash;75.-Perzentil, Linie = Median, Whisker = Min/Max.</div>
    </div>
  </section>
</main>
<div class="tt" id="tt"></div>

<script>
const DATA = /*__DATA__*/;
const NS = "http://www.w3.org/2000/svg";
const FARBEN = DATA.meta.farben;
const MODELLE = DATA.meta.modelle;
const HORIZONTE = DATA.meta.horizonte;
const tt = document.getElementById("tt");

function svgEl(t,a,kids){const e=document.createElementNS(NS,t);for(const k in (a||{}))e.setAttribute(k,a[k]);
  (kids||[]).forEach(c=>e.appendChild(c));return e;}
function clr(el){while(el.firstChild)el.removeChild(el.firstChild);}
function fmt(v,d){if(v==null||isNaN(v))return "-";return Number(v).toFixed(d==null?2:d);}
function mean(a){return a.length?a.reduce((s,x)=>s+x,0)/a.length:NaN;}
function showTT(html,x,y){tt.innerHTML=html;tt.style.display="block";tt.style.left=(x+14)+"px";tt.style.top=(y+14)+"px";}
function hideTT(){tt.style.display="none";}

/* ---------- Tabs ---------- */
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));
  t.classList.add("active");
  const id=t.dataset.tab;
  document.getElementById("tab-fehler").style.display = id=="fehler"?"":"none";
  document.getElementById("tab-kurven").style.display = id=="kurven"?"":"none";
  document.getElementById("tab-vert").style.display  = id=="vert"?"":"none";
});

/* ---------- Chip- / Select-Helfer ---------- */
function baueModellChips(container, state){
  clr(container);
  MODELLE.forEach(m=>{
    const chip=document.createElement("div");
    chip.className="chip"+(state.has(m)?"":" off");
    chip.innerHTML=`<span class="dot" style="background:${FARBEN[m]||'#888'}"></span>${m}`;
    chip.onclick=()=>{ if(state.has(m))state.delete(m); else state.add(m);
      chip.classList.toggle("off"); container.dispatchEvent(new Event("change")); };
    container.appendChild(chip);
  });
}
function fuelleSelect(sel, opts){ clr(sel); opts.forEach(o=>{const e=document.createElement("option");
  e.value=o;e.textContent=o;sel.appendChild(e);}); }
function radio(container, onChange){
  container.querySelectorAll("button").forEach(b=>b.onclick=()=>{
    container.querySelectorAll("button").forEach(x=>x.classList.remove("active"));
    b.classList.add("active"); onChange(b.dataset.v);
  });
}

/* ======================================================= TAB 1: Fehlervergleich */
const F = {metrik:"MASE", station:"Alle", modelle:new Set(MODELLE)};
(function initF(){
  fuelleSelect(document.getElementById("f-station"), ["Alle", ...DATA.meta.stationen]);
  document.getElementById("f-station").onchange=e=>{F.station=e.target.value;zeichneF();};
  radio(document.getElementById("f-metrik"), v=>{F.metrik=v;zeichneF();});
  const box=document.getElementById("f-modelle");
  baueModellChips(box, F.modelle); box.addEventListener("change",zeichneF);
  zeichneF();
})();

function aggMetrik(metrik, station){
  // Mittel je (Horizont, Modell) ueber Folds (und Stationen, falls "Alle")
  const acc={};
  DATA.metriken.forEach(r=>{
    if(station!="Alle" && r.Station!=station) return;
    const k=r.Horizont+"|"+r.Modell;
    (acc[k]=acc[k]||[]).push(r[metrik]);
  });
  const out={};
  for(const k in acc){ out[k]=mean(acc[k]); }
  return out;
}

function zeichneF(){
  const svg=document.getElementById("f-chart"); clr(svg);
  const W=960,H=440,mL=58,mR=16,mT=18,mB=54;
  const plotW=W-mL-mR, plotH=H-mT-mB;
  const modelle=MODELLE.filter(m=>F.modelle.has(m));
  const agg=aggMetrik(F.metrik, F.station);
  let maxV=0; HORIZONTE.forEach(h=>modelle.forEach(m=>{const v=agg[h+"|"+m];if(v>maxV)maxV=v;}));
  maxV=maxV*1.12||1;
  const x0=h=>mL+plotW*(HORIZONTE.indexOf(h))/HORIZONTE.length;
  const gw=plotW/HORIZONTE.length;
  const bw=Math.min(46,(gw-16)/Math.max(modelle.length,1));
  const yPix=v=>mT+plotH*(1-v/maxV);
  // Achsen + Gitter
  for(let i=0;i<=5;i++){const v=maxV*i/5,y=yPix(v);
    svg.appendChild(svgEl("line",{x1:mL,y1:y,x2:W-mR,y2:y,stroke:"#2a3348","stroke-width":1}));
    svg.appendChild(svgEl("text",{x:mL-8,y:y+4,fill:"#9aa7bd","font-size":11,"text-anchor":"end"},[txt(fmt(v,1))]));}
  if(F.metrik=="MASE" && 1<maxV){const y=yPix(1);
    svg.appendChild(svgEl("line",{x1:mL,y1:y,x2:W-mR,y2:y,stroke:"#C4471C","stroke-width":1.5,"stroke-dasharray":"6 4"}));}
  HORIZONTE.forEach(h=>{
    const gx=x0(h)+gw/2;
    svg.appendChild(svgEl("text",{x:gx,y:H-mB+22,fill:"#e8ecf4","font-size":12,"text-anchor":"middle"},[txt(h+" h")]));
    modelle.forEach((m,mi)=>{
      const v=agg[h+"|"+m]; if(v==null||isNaN(v))return;
      const bx=x0(h)+gw/2-(modelle.length*bw)/2+mi*bw;
      const by=yPix(v), bh=mT+plotH-by;
      const rect=svgEl("rect",{x:bx,y:by,width:bw-3,height:bh,fill:FARBEN[m]||"#888",rx:3});
      rect.addEventListener("mousemove",e=>showTT(`<b>${m}</b><br>${h} h &middot; ${F.metrik}<br><b>${fmt(v,F.metrik=='MASE'?3:2)}</b>`,e.clientX,e.clientY));
      rect.addEventListener("mouseleave",hideTT);
      svg.appendChild(rect);
    });
  });
  // Achsentitel
  svg.appendChild(svgEl("text",{x:16,y:mT+plotH/2,fill:"#9aa7bd","font-size":12,"text-anchor":"middle",transform:`rotate(-90 16 ${mT+plotH/2})`},[txt(F.metrik==="MAPE"?"MAPE %":F.metrik)]));
  document.getElementById("f-hint").textContent =
    F.metrik=="MASE" ? "MASE < 1 bedeutet besser als die Seasonal-Naive-Baseline (rote Linie)." : "";
  tabelleF(agg, modelle);
}
function tabelleF(agg, modelle){
  const t=document.getElementById("f-table"); clr(t);
  const thead=document.createElement("tr"); thead.appendChild(th("Modell \\ Horizont"));
  HORIZONTE.forEach(h=>thead.appendChild(th(h+" h"))); t.appendChild(thead);
  modelle.forEach(m=>{const tr=document.createElement("tr");
    const c0=document.createElement("td");c0.innerHTML=`<span style="color:${FARBEN[m]}">&#9632;</span> ${m}`;tr.appendChild(c0);
    HORIZONTE.forEach(h=>{const v=agg[h+"|"+m];tr.appendChild(td(fmt(v,F.metrik=='MASE'?3:2)));});
    t.appendChild(tr);});
}
function th(s){const e=document.createElement("th");e.textContent=s;return e;}
function td(s){const e=document.createElement("td");e.textContent=s;return e;}
function txt(s){return document.createTextNode(s);}

/* ======================================================= TAB 2: Prognosekurven */
const K={station:null,fold:null,hor:72,modelle:new Set(MODELLE)};
(function initK(){
  if(!DATA.meta.hat_kurven){
    document.getElementById("kurven-panel").innerHTML =
      '<div class="warn">Noch keine Kurvendaten vorhanden. Bitte im Notebook 05 <b>Abschnitt 9d</b> ausf&uuml;hren '+
      '(schreibt <code>vorhersagen_rolling.csv</code>) und danach dieses Dashboard neu bauen.</div>';
    return;
  }
  K.station=DATA.meta.stationen[0]; K.fold=DATA.meta.folds[0];
  fuelleSelect(document.getElementById("k-station"),DATA.meta.stationen);
  fuelleSelect(document.getElementById("k-fold"),DATA.meta.folds);
  document.getElementById("k-station").onchange=e=>{K.station=e.target.value;zeichneK();};
  document.getElementById("k-fold").onchange=e=>{K.fold=e.target.value;zeichneK();};
  radio(document.getElementById("k-hor"),v=>{K.hor=+v;zeichneK();});
  const box=document.getElementById("k-modelle"); baueModellChips(box,K.modelle);
  box.addEventListener("change",zeichneK);
  zeichneK();
})();

function zeichneK(){
  const svg=document.getElementById("k-chart"); clr(svg);
  const key=K.fold+"|"+K.station; const cur=DATA.kurven[key];
  const leg=document.getElementById("k-legend"); clr(leg);
  if(!cur){document.getElementById("k-hint").textContent="Keine Daten fuer diese Kombination.";return;}
  const n=cur.lead.filter(l=>l<K.hor).length;  // lead ist 0-basiert (Stunden ab Fold-Start)
  const idx=[...Array(cur.lead.length).keys()].filter(i=>cur.lead[i]<K.hor);
  const W=960,H=430,mL=56,mR=16,mT=16,mB=44, plotW=W-mL-mR, plotH=H-mT-mB;
  const modelle=MODELLE.filter(m=>K.modelle.has(m) && cur.series[m]);
  let maxV=Math.max(...idx.map(i=>cur.y[i]));
  modelle.forEach(m=>idx.forEach(i=>{const v=cur.series[m][i]; if(v>maxV)maxV=v;}));
  maxV=maxV*1.1||1;
  const xPix=j=>mL+plotW*j/Math.max(idx.length-1,1);
  const yPix=v=>mT+plotH*(1-v/maxV);
  for(let i=0;i<=5;i++){const v=maxV*i/5,y=yPix(v);
    svg.appendChild(svgEl("line",{x1:mL,y1:y,x2:W-mR,y2:y,stroke:"#2a3348","stroke-width":1}));
    svg.appendChild(svgEl("text",{x:mL-8,y:y+4,fill:"#9aa7bd","font-size":11,"text-anchor":"end"},[txt(fmt(v,0))]));}
  // x-Ticks alle ~12h
  idx.forEach((i,j)=>{ if(cur.lead[i]%12===0){ const x=xPix(j);
    svg.appendChild(svgEl("line",{x1:x,y1:mT+plotH,x2:x,y2:mT+plotH+5,stroke:"#9aa7bd"}));
    svg.appendChild(svgEl("text",{x:x,y:H-mB+20,fill:"#9aa7bd","font-size":11,"text-anchor":"middle"},[txt("+"+cur.lead[i]+"h")]));}});
  // echte Werte
  polyline(svg, idx.map((i,j)=>[xPix(j),yPix(cur.y[i])]), "#e8ecf4", 2.6);
  legItem(leg,"Echte Werte","#e8ecf4");
  const maes={};
  modelle.forEach(m=>{
    const pts=idx.map((i,j)=>[xPix(j),yPix(cur.series[m][i])]);
    polyline(svg,pts,FARBEN[m]||"#888",1.8);
    maes[m]=mean(idx.map(i=>Math.abs(cur.y[i]-cur.series[m][i])));
    legItem(leg,`${m} (MAE ${fmt(maes[m],1)})`,FARBEN[m]||"#888");
  });
  // Hover-Overlay
  const ov=svgEl("rect",{x:mL,y:mT,width:plotW,height:plotH,fill:"transparent"});
  const guide=svgEl("line",{x1:mL,y1:mT,x2:mL,y2:mT+plotH,stroke:"#6b7891","stroke-width":1,"stroke-dasharray":"3 3",opacity:0});
  svg.appendChild(guide); svg.appendChild(ov);
  ov.addEventListener("mousemove",e=>{
    const r=svg.getBoundingClientRect(); const px=(e.clientX-r.left)/r.width*W;
    let j=Math.round((px-mL)/plotW*(idx.length-1)); j=Math.max(0,Math.min(idx.length-1,j));
    const i=idx[j]; const gx=xPix(j); guide.setAttribute("x1",gx);guide.setAttribute("x2",gx);guide.setAttribute("opacity",1);
    let html=`<b>+${cur.lead[i]} h</b> &middot; ${cur.ds[i]}<br>Echt: <b>${fmt(cur.y[i],1)}</b>`;
    modelle.forEach(m=>html+=`<br><span style="color:${FARBEN[m]}">&#9632;</span> ${m}: ${fmt(cur.series[m][i],1)}`);
    showTT(html,e.clientX,e.clientY);
  });
  ov.addEventListener("mouseleave",()=>{hideTT();guide.setAttribute("opacity",0);});
  svg.appendChild(svgEl("text",{x:16,y:mT+plotH/2,fill:"#9aa7bd","font-size":12,"text-anchor":"middle",transform:`rotate(-90 16 ${mT+plotH/2})`},[txt("PM2.5 (µg/m³)")]));
  document.getElementById("k-hint").textContent =
    `Station ${K.station}, Fold-Start ${K.fold}, Horizont ${K.hor} h. MAE je Modell in der Legende (nur dieses Fenster).`;
}
function polyline(svg,pts,color,w){
  const d=pts.map((p,i)=>(i?"L":"M")+p[0].toFixed(1)+" "+p[1].toFixed(1)).join(" ");
  svg.appendChild(svgEl("path",{d:d,fill:"none",stroke:color,"stroke-width":w,"stroke-linejoin":"round"}));
}
function legItem(leg,label,color){const d=document.createElement("div");d.className="it";
  d.innerHTML=`<span class="sw" style="background:${color}"></span>${label}`;leg.appendChild(d);}

/* ======================================================= TAB 3: MASE-Verteilung */
const V={hor:72,modelle:new Set(MODELLE)};
(function initV(){
  radio(document.getElementById("v-hor"),v=>{V.hor=+v;zeichneV();});
  const box=document.getElementById("v-modelle"); baueModellChips(box,V.modelle);
  box.addEventListener("change",zeichneV);
  zeichneV();
})();
function quantil(sorted,q){const pos=(sorted.length-1)*q,b=Math.floor(pos),r=pos-b;
  return sorted[b+1]!==undefined?sorted[b]+r*(sorted[b+1]-sorted[b]):sorted[b];}
function zeichneV(){
  const svg=document.getElementById("v-chart"); clr(svg);
  const modelle=MODELLE.filter(m=>V.modelle.has(m));
  const werte={}; modelle.forEach(m=>werte[m]=[]);
  DATA.metriken.forEach(r=>{ if(r.Horizont===V.hor && werte[r.Modell]) werte[r.Modell].push(r.MASE); });
  const W=960,H=420,mL=56,mR=16,mT=16,mB=54, plotW=W-mL-mR, plotH=H-mT-mB;
  let maxV=0; modelle.forEach(m=>werte[m].forEach(v=>{if(v>maxV)maxV=v;})); maxV=maxV*1.12||1;
  const yPix=v=>mT+plotH*(1-v/maxV);
  for(let i=0;i<=5;i++){const v=maxV*i/5,y=yPix(v);
    svg.appendChild(svgEl("line",{x1:mL,y1:y,x2:W-mR,y2:y,stroke:"#2a3348"}));
    svg.appendChild(svgEl("text",{x:mL-8,y:y+4,fill:"#9aa7bd","font-size":11,"text-anchor":"end"},[txt(fmt(v,1))]));}
  if(1<maxV){const y=yPix(1);svg.appendChild(svgEl("line",{x1:mL,y1:y,x2:W-mR,y2:y,stroke:"#C4471C","stroke-width":1.5,"stroke-dasharray":"6 4"}));}
  const gw=plotW/Math.max(modelle.length,1);
  modelle.forEach((m,mi)=>{
    const arr=werte[m].slice().sort((a,b)=>a-b); if(!arr.length)return;
    const cx=mL+gw*(mi+0.5), bw=Math.min(70,gw*0.5);
    const q1=quantil(arr,.25),md=quantil(arr,.5),q3=quantil(arr,.75),lo=arr[0],hi=arr[arr.length-1];
    const col=FARBEN[m]||"#888";
    svg.appendChild(svgEl("line",{x1:cx,y1:yPix(lo),x2:cx,y2:yPix(hi),stroke:col,"stroke-width":1.5}));
    svg.appendChild(svgEl("line",{x1:cx-bw/3,y1:yPix(lo),x2:cx+bw/3,y2:yPix(lo),stroke:col}));
    svg.appendChild(svgEl("line",{x1:cx-bw/3,y1:yPix(hi),x2:cx+bw/3,y2:yPix(hi),stroke:col}));
    const box=svgEl("rect",{x:cx-bw/2,y:yPix(q3),width:bw,height:Math.max(yPix(q1)-yPix(q3),1),
      fill:col,"fill-opacity":.35,stroke:col,"stroke-width":1.5,rx:3});
    box.addEventListener("mousemove",e=>showTT(`<b>${m}</b> &middot; ${V.hor} h<br>Median ${fmt(md,3)}<br>Q1 ${fmt(q1,3)} &middot; Q3 ${fmt(q3,3)}<br>Min ${fmt(lo,3)} &middot; Max ${fmt(hi,3)}`,e.clientX,e.clientY));
    box.addEventListener("mouseleave",hideTT);
    svg.appendChild(box);
    svg.appendChild(svgEl("line",{x1:cx-bw/2,y1:yPix(md),x2:cx+bw/2,y2:yPix(md),stroke:col,"stroke-width":2.5}));
    svg.appendChild(svgEl("text",{x:cx,y:H-mB+20,fill:"#e8ecf4","font-size":12,"text-anchor":"middle"},[txt(m)]));
  });
  svg.appendChild(svgEl("text",{x:16,y:mT+plotH/2,fill:"#9aa7bd","font-size":12,"text-anchor":"middle",transform:`rotate(-90 16 ${mT+plotH/2})`},[txt("MASE")]));
}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
