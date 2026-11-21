# Génère les SVG animés du README de profil GitHub
import os, sys, textwrap
from xml.sax.saxutils import escape as esc

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Cascadia Code', Consolas, 'SF Mono', Menlo, 'Courier New', monospace"
V, M, O, C, G, B = "#8b5cf6", "#ec4899", "#f97316", "#22d3ee", "#34d399", "#3b82f6"
TXT, MUTED, CARD, LINE = "#f3f1ff", "#a49fc2", "#0f0b1e", "#2a2342"

ICONS = {
    "globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
    "mail": '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
    "github": '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "cloud": '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/>',
    "layout": '<rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    "award": '<circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>',
    "message": '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/>',
    "folder": '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
    "arrow": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
}

def icon(name, x, y, size=24, color="#fff", sw=2, cls=""):
    s = size / 24
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')

def svg(w, h, body, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>text{{font-family:{SANS}}} .mono{{font-family:{MONO}}} {style}</style>{body}</svg>')

def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf8") as f:
        f.write(content)

def grad(id_, *cols, x2=1, y2=0, anim=False):
    stops = "".join(f'<stop offset="{i/(len(cols)-1):.2f}" stop-color="{c}"/>' for i, c in enumerate(cols))
    a = ('<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="8s" repeatCount="indefinite"/>'
         if anim else "")
    sm = ' spreadMethod="reflect"' if anim else ""
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}"{sm}>{stops}{a}</linearGradient>'

def tw(s, size, k=0.56):  # largeur de texte approximative
    return len(s) * size * k

# ============================== HEADER ==============================
def header():
    W, H = 1200, 430
    layers = [[95, 175, 255, 335], [70, 150, 230, 310, 390], [110, 210, 310], [160, 260]]
    xs = [800, 900, 1000, 1100]
    cols = [V, M, C, O]
    edges, nodes = [], []
    k = 0
    for li in range(len(layers) - 1):
        for y1 in layers[li]:
            for y2 in layers[li + 1]:
                k += 1
                edges.append(f'<line class="edge" style="animation-delay:-{(k*0.37)%3:.2f}s" x1="{xs[li]}" y1="{y1}" x2="{xs[li+1]}" y2="{y2}" stroke="url(#edge)" stroke-width="1.2"/>')
    k = 0
    for li, ys in enumerate(layers):
        for y in ys:
            k += 1
            c = cols[li]
            nodes.append(f'<circle cx="{xs[li]}" cy="{y}" r="13" fill="{c}" opacity=".12"/>'
                         f'<circle class="node" style="animation-delay:-{(k*0.41)%2.4:.2f}s" cx="{xs[li]}" cy="{y}" r="6" fill="{c}"/>')
    roles = ["Data Analyst", "Data Scientist Junior", "ML Engineer", "Développeuse Web"]
    roles_svg = "".join(f'<text class="mono role" style="animation-delay:{i*3}s" x="72" y="322" font-size="26" fill="{TXT}"><tspan fill="{C}">›</tspan> {esc(r)}</text>' for i, r in enumerate(roles))
    chips, x = [], 72
    for label, dot in [("Ouverte aux opportunités", G), ("Dakar · Sénégal", O), ("Orange Digital Center", M)]:
        w = tw(label, 14, .55) + 44
        chips.append(f'<g class="fade" style="animation-delay:{.8+len(chips)*.15}s"><rect x="{x}" y="352" width="{w:.0f}" height="34" rx="17" fill="#ffffff" fill-opacity=".06" stroke="#ffffff" stroke-opacity=".14"/>'
                     f'<circle class="{"live" if dot==G else ""}" cx="{x+18}" cy="369" r="5" fill="{dot}"/>'
                     f'<text x="{x+32}" y="374" font-size="14" fill="{TXT}">{esc(label)}</text></g>')
        x += w + 12
    body = f'''
<defs>
  {grad("bg", "#0b0816", "#150a2b", "#0a1022", x2=1, y2=1)}
  {grad("tg", V, M, O, anim=True)}
  {grad("edge", V, M, C)}
  {grad("bd", V, M, O, C)}
  <radialGradient id="b1"><stop offset="0" stop-color="{V}" stop-opacity=".55"/><stop offset="1" stop-color="{V}" stop-opacity="0"/></radialGradient>
  <radialGradient id="b2"><stop offset="0" stop-color="{M}" stop-opacity=".45"/><stop offset="1" stop-color="{M}" stop-opacity="0"/></radialGradient>
  <radialGradient id="b3"><stop offset="0" stop-color="{C}" stop-opacity=".3"/><stop offset="1" stop-color="{C}" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity=".045"/></pattern>
  <clipPath id="r"><rect width="{W}" height="{H}" rx="26"/></clipPath>
  <filter id="blur"><feGaussianBlur stdDeviation="14"/></filter>
</defs>
<g clip-path="url(#r)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <circle class="blob" cx="160" cy="40" r="300" fill="url(#b1)"/>
  <circle class="blob" style="animation-delay:-5s" cx="1050" cy="420" r="320" fill="url(#b2)"/>
  <circle class="blob" style="animation-delay:-9s" cx="640" cy="-20" r="260" fill="url(#b3)"/>
  <rect class="scan" x="0" y="0" width="{W}" height="2" fill="url(#bd)" opacity=".35"/>
  <g class="ring"><circle cx="950" cy="230" r="190" fill="none" stroke="url(#bd)" stroke-width="1.5" stroke-dasharray="2 14" opacity=".55"/>
  <circle cx="950" cy="230" r="215" fill="none" stroke="{C}" stroke-width="1" stroke-dasharray="80 260" opacity=".4"/></g>
  {"".join(edges)}
  {"".join(nodes)}
  <text class="mono fade" x="72" y="112" font-size="19" fill="{C}">&gt; hello world, je suis<tspan class="caret" fill="{M}"> ▌</tspan></text>
  <text class="fade" style="animation-delay:.15s" x="70" y="190" font-size="66" font-weight="800" fill="{TXT}" letter-spacing="-1.5">Yaye Amanatou</text>
  <text x="68" y="276" font-size="92" font-weight="900" fill="url(#tg)" letter-spacing="-2" filter="url(#blur)" opacity=".55">NDIAYE</text>
  <text class="fade" style="animation-delay:.3s" x="68" y="276" font-size="92" font-weight="900" fill="url(#tg)" letter-spacing="-2">NDIAYE</text>
  {roles_svg}
  {"".join(chips)}
</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="26" fill="none" stroke="url(#bd)" stroke-opacity=".7" stroke-width="1.5"/>'''
    style = '''
.blob{animation:drift 14s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center}
@keyframes drift{to{transform:translate(70px,40px) scale(1.18)}}
.edge{stroke-dasharray:5 11;opacity:.55;animation:flow 3s linear infinite}
@keyframes flow{to{stroke-dashoffset:-64}}
.node{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-in-out infinite}
@keyframes pulse{50%{transform:scale(1.55);opacity:.55}}
.ring{transform-origin:950px 230px;animation:spin 24s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.role{opacity:0;animation:roles 12s infinite}
@keyframes roles{0%{opacity:0;transform:translateY(14px)}4%,21%{opacity:1;transform:none}25%,100%{opacity:0;transform:translateY(-14px)}}
.fade{animation:fadeup 1s ease-out both}
@keyframes fadeup{from{opacity:0;transform:translateY(18px)}}
.caret{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}
.live{transform-box:fill-box;transform-origin:center;animation:pulse 2s infinite}
.scan{animation:scan 7s linear infinite}@keyframes scan{from{transform:translateY(-10px)}to{transform:translateY(440px)}}'''
    write("header.svg", svg(W, H, body, style))

# ============================== BOUTONS ==============================
def button(name, label, ic, c1, c2, c3=None, primary=False):
    H = 64
    W = int(tw(label, 17, .64) + 118)
    cols = [c1, c2] + ([c3] if c3 else [])
    fill = "url(#g)" if primary else "#120c22"
    stroke = "" if primary else 'stroke="url(#g)" stroke-width="2"'
    body = f'''
<defs>{grad("g", *cols, anim=True)}
<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity="{.55 if primary else .28}"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="p"><rect x="6" y="8" width="{W-12}" height="48" rx="24"/></clipPath>
<filter id="gl" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="6"/></filter></defs>
<rect class="halo" x="10" y="12" width="{W-20}" height="44" rx="22" fill="url(#g)" filter="url(#gl)"/>
<rect x="6" y="8" width="{W-12}" height="48" rx="24" fill="{fill}" {stroke}/>
<g clip-path="url(#p)"><rect class="sh" x="-90" y="0" width="70" height="{H}" fill="url(#sh)"/></g>
<circle cx="36" cy="32" r="16" fill="#fff" fill-opacity="{.18 if primary else .07}"/>
{icon(ic, 27, 23, 18, "#fff" if primary else c1)}
<text x="62" y="38" font-size="17" font-weight="700" fill="#fff">{esc(label)}</text>
<g class="ar">{icon("arrow", W-42, 24, 16, "#fff", 2.4)}</g>'''
    style = f'''.sh{{animation:sh 3.4s ease-in-out infinite}}
@keyframes sh{{0%{{transform:translateX(0) skewX(-20deg)}}55%,100%{{transform:translateX({W+120}px) skewX(-20deg)}}}}
.ar{{animation:ar 1.6s ease-in-out infinite}}@keyframes ar{{50%{{transform:translateX(5px)}}}}
.halo{{opacity:{.55 if primary else .35};animation:halo 2.8s ease-in-out infinite}}@keyframes halo{{50%{{opacity:{.9 if primary else .6}}}}}'''
    write(f"btn-{name}.svg", svg(W, H, body, style))

# ============================== TITRES ==============================
def title(name, num, label):
    W, H = 1000, 76
    tx = 64
    end = tx + tw(label, 32, .6) + 24
    body = f'''<defs>{grad("t", V, M, O, anim=True)}
<linearGradient id="l" gradientUnits="userSpaceOnUse" x1="{end:.0f}" y1="0" x2="{W}" y2="0"><stop offset="0" stop-color="{M}"/><stop offset="1" stop-color="{V}" stop-opacity="0"/></linearGradient></defs>
<rect x="0" y="16" width="46" height="46" rx="14" fill="{V}" fill-opacity=".14" stroke="url(#t)" stroke-width="1.5"/>
<text class="mono" x="23" y="45" font-size="16" font-weight="700" fill="{M}" text-anchor="middle">{num}</text>
<text x="{tx}" y="51" font-size="32" font-weight="800" fill="url(#t)" letter-spacing="-.5">{esc(label)}</text>
<line x1="{end:.0f}" y1="40" x2="{W}" y2="40" stroke="url(#l)" stroke-width="1.5"/>
<circle r="4" cy="40" fill="{M}"><animate attributeName="cx" values="{end:.0f};{W-60};{end:.0f}" dur="5s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="1;.2;1" dur="5s" repeatCount="indefinite"/></circle>'''
    write(f"title-{name}.svg", svg(W, H, body))

# ============================== TERMINAL ==============================
def terminal():
    W, H = 560, 400
    seq = [
        ("cmd", "whoami"),
        ("out", "Yaye Amanatou NDIAYE", TXT, True),
        ("cmd", "cat roles.txt"),
        ("out", "Data Analyst · Data Scientist Jr · ML Engineer", M, False),
        ("cmd", "ls ./stack"),
        ("out", "python  pandas  sklearn  tensorflow  llm  rag", C, False),
        ("cmd", "cat now.txt"),
        ("out", "CPS Référent IA @ Orange Digital Center", G, False),
        ("cmd", "echo $MISSION"),
        ("out", "Innover pour l'Afrique avec la data & l'IA", O, False),
    ]
    parts, defs, t, y = [], [], 0.6, 84
    for i, item in enumerate(seq):
        if item[0] == "cmd":
            cmd = item[1]
            dur = max(0.4, len(cmd) * 0.07)
            defs.append(f'<clipPath id="c{i}"><rect x="0" y="{y-20}" height="28" width="0"><animate attributeName="width" from="0" to="{W}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
            parts.append(f'<g clip-path="url(#c{i})"><text class="mono" x="26" y="{y}" font-size="15"><tspan fill="{C}">~</tspan><tspan fill="{M}"> $ </tspan><tspan fill="{TXT}">{esc(cmd)}</tspan></text></g>')
            t += dur + 0.25
        else:
            _, txt, col, bold = item
            parts.append(f'<text class="mono" x="26" y="{y}" font-size="15" fill="{col}" font-weight="{700 if bold else 400}" opacity="0">'
                         f'<tspan fill="{MUTED}">› </tspan>{esc(txt)}<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".3s" fill="freeze"/></text>')
            t += 0.55
        y += 28
    parts.append(f'<text class="mono" x="26" y="{y}" font-size="15" opacity="0"><tspan fill="{C}">~</tspan><tspan fill="{M}"> $ </tspan>'
                 f'<tspan class="caret" fill="{TXT}">▌</tspan><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".2s" fill="freeze"/></text>')
    body = f'''<defs>{"".join(defs)}{grad("bd", V, M, O)}
<radialGradient id="gl"><stop offset="0" stop-color="{V}" stop-opacity=".35"/><stop offset="1" stop-color="{V}" stop-opacity="0"/></radialGradient>
<clipPath id="win"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
<g clip-path="url(#win)">
<rect width="{W}" height="{H}" fill="#0c0919"/>
<circle cx="{W}" cy="{H}" r="260" fill="url(#gl)"/>
<rect width="{W}" height="42" fill="#ffffff" fill-opacity=".04"/>
<circle cx="24" cy="21" r="6.5" fill="#ff5f57"/><circle cx="46" cy="21" r="6.5" fill="#febc2e"/><circle cx="68" cy="21" r="6.5" fill="#28c840"/>
<text class="mono" x="{W/2}" y="26" font-size="13" fill="{MUTED}" text-anchor="middle">amanatou@dakar: ~</text>
{"".join(parts)}
</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="18" fill="none" stroke="url(#bd)" stroke-opacity=".6" stroke-width="1.5"/>'''
    write("terminal.svg", svg(W, H, body, ".caret{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"))

# ============================== FOCUS ==============================
def focus():
    W, H = 560, 400
    rows = [
        ("cpu", G, "EN CE MOMENT", "CPS Référent IA — Orange Digital Center"),
        ("compass", C, "J'EXPLORE", "LLM, RAG, Agents IA & MLOps"),
        ("award", O, "DERNIER DÉFI", "PAS Challenge SALSTIS 2026 — JOJ Dakar"),
        ("message", M, "PARLONS DE", "Data, IA & innovation en Afrique"),
        ("globe", V, "LANGUES", "Français · English · Wolof"),
    ]
    out, y = [], 78
    for i, (ic, col, lab, val) in enumerate(rows):
        out.append(f'<g class="row" style="animation-delay:{.3+i*.18:.2f}s">'
                   f'<rect x="22" y="{y}" width="{W-44}" height="54" rx="14" fill="#fff" fill-opacity=".035" stroke="#fff" stroke-opacity=".07"/>'
                   f'<rect x="34" y="{y+9}" width="36" height="36" rx="11" fill="{col}" fill-opacity=".16" stroke="{col}" stroke-opacity=".5"/>'
                   f'{icon(ic, 43, y+18, 18, col)}'
                   f'<text class="mono" x="86" y="{y+22}" font-size="11" letter-spacing="1.2" fill="{col}">{esc(lab)}</text>'
                   f'<text x="86" y="{y+42}" font-size="16" font-weight="600" fill="{TXT}">{esc(val)}</text></g>')
        y += 62
    body = f'''<defs>{grad("bd", C, V, M)}
<radialGradient id="gl"><stop offset="0" stop-color="{M}" stop-opacity=".3"/><stop offset="1" stop-color="{M}" stop-opacity="0"/></radialGradient>
<clipPath id="win"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
<g clip-path="url(#win)"><rect width="{W}" height="{H}" fill="#0c0919"/>
<circle cx="0" cy="0" r="260" fill="url(#gl)"/>
<text x="24" y="48" font-size="22" font-weight="800" fill="{TXT}">En ce moment<tspan fill="{M}">.</tspan></text>
<rect x="{W-96}" y="27" width="72" height="26" rx="13" fill="{G}" fill-opacity=".14" stroke="{G}" stroke-opacity=".5"/>
<circle class="live" cx="{W-80}" cy="40" r="4.5" fill="{G}"/>
<text class="mono" x="{W-68}" y="45" font-size="12" font-weight="700" fill="{G}">LIVE</text>
{"".join(out)}</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="18" fill="none" stroke="url(#bd)" stroke-opacity=".6" stroke-width="1.5"/>'''
    style = '''.row{animation:in .7s ease-out both}@keyframes in{from{opacity:0;transform:translateX(-24px)}}
.live{transform-box:fill-box;transform-origin:center;animation:p 1.6s infinite}@keyframes p{50%{transform:scale(1.7);opacity:.4}}'''
    write("focus.svg", svg(W, H, body, style))

# ============================== TIMELINE ==============================
def timeline():
    W, H = 1000, 250
    items = [
        ("2021 — 22", "Bac S2", "Lycée Ameth Fall · Saint-Louis", C),
        ("2022 — 26", "Licence Informatique", "UASZ · Ziguinchor", V),
        ("Mai — Août 2026", "Stage gestion de caisse", "KAY YIWU SHOP · Dakar", B),
        ("2026", "Challenge SALSTIS", "JOJ Dakar 2026 · Innovation", O),
        ("Juil. 2026 →", "CPS Référent IA", "Orange Digital Center", M),
    ]
    xs = [100, 300, 500, 700, 900]
    out = []
    for i, ((date, t, sub, col), x) in enumerate(zip(items, xs)):
        d = .4 + i * .45
        last = i == len(items) - 1
        out.append(f'<g class="it" style="animation-delay:{d:.2f}s">'
                   f'<text class="mono" x="{x}" y="78" font-size="13" font-weight="700" fill="{col}" text-anchor="middle">{esc(date)}</text>'
                   f'<circle cx="{x}" cy="120" r="20" fill="{col}" fill-opacity=".12"/>'
                   + (f'<circle class="live" cx="{x}" cy="120" r="20" fill="none" stroke="{col}" stroke-width="2"/>' if last else "")
                   + f'<circle cx="{x}" cy="120" r="9" fill="#0c0919" stroke="{col}" stroke-width="3"/>'
                   f'<text x="{x}" y="168" font-size="16" font-weight="700" fill="{TXT}" text-anchor="middle">{esc(t)}</text>'
                   f'<text x="{x}" y="190" font-size="12.5" fill="{MUTED}" text-anchor="middle">{esc(sub)}</text>'
                   + (f'<rect x="{x-38}" y="202" width="76" height="22" rx="11" fill="{G}" fill-opacity=".15"/><text class="mono" x="{x}" y="217" font-size="11" font-weight="700" fill="{G}" text-anchor="middle">EN COURS</text>' if last else "")
                   + '</g>')
    body = f'''<defs><linearGradient id="ln" gradientUnits="userSpaceOnUse" x1="60" y1="0" x2="940" y2="0"><stop offset="0" stop-color="{C}"/><stop offset=".25" stop-color="{V}"/><stop offset=".5" stop-color="{B}"/><stop offset=".75" stop-color="{O}"/><stop offset="1" stop-color="{M}"/></linearGradient>
<clipPath id="win"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
<g clip-path="url(#win)"><rect width="{W}" height="{H}" fill="#0c0919"/>
<line x1="60" y1="120" x2="940" y2="120" stroke="#fff" stroke-opacity=".08" stroke-width="4" stroke-linecap="round"/>
<line class="draw" x1="60" y1="120" x2="940" y2="120" stroke="url(#ln)" stroke-width="4" stroke-linecap="round"/>
<circle r="5" cy="120" fill="#fff"><animate attributeName="cx" values="60;940" dur="4s" begin="2.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" dur="4s" begin="2.6s" repeatCount="indefinite"/></circle>
{"".join(out)}</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="18" fill="none" stroke="url(#ln)" stroke-opacity=".5" stroke-width="1.5"/>'''
    style = '''.draw{stroke-dasharray:880;stroke-dashoffset:880;animation:draw 2.6s ease-out .2s forwards}@keyframes draw{to{stroke-dashoffset:0}}
.it{animation:in .7s ease-out both}@keyframes in{from{opacity:0;transform:translateY(16px)}}
.live{transform-box:fill-box;transform-origin:center;animation:p 1.8s infinite}@keyframes p{from{transform:scale(.6);opacity:1}to{transform:scale(1.8);opacity:0}}'''
    write("timeline.svg", svg(W, H, body, style))

# ============================== AI STACK ==============================
def ai_stack():
    W = 1000
    items = ["Pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter", "BeautifulSoup", "Excel (TCD)",
             "Keras", "NLP / TF-IDF", "Computer Vision", "LLM", "RAG", "Prompt Engineering",
             "Embeddings", "ChromaDB", "Wireshark", "OpenSSL", "Nagios / SNMP", "Agile / Scrum"]
    cols = [C, V, M, O, G]
    PAD = 26
    out, x, y = [], 0, PAD
    rows = []
    row = []
    for it in items:
        w = tw(it, 14.5, .56) + 44
        if x + w > W - 2 * PAD and row:
            rows.append((row, x - 10)); row, x = [], 0
        row.append((it, w, x)); x += w + 10
    rows.append((row, x - 10))
    k = 0
    for row, rw in rows:
        off = (W - rw) / 2
        for it, w, rx in row:
            col = cols[k % len(cols)]
            out.append(f'<g class="pill" style="animation-delay:{k*.07:.2f}s">'
                       f'<rect x="{off+rx:.0f}" y="{y}" width="{w:.0f}" height="38" rx="19" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-opacity=".55"/>'
                       f'<circle cx="{off+rx+18:.0f}" cy="{y+19}" r="4" fill="{col}"/>'
                       f'<text x="{off+rx+30:.0f}" y="{y+24}" font-size="14.5" font-weight="600" fill="{TXT}">{esc(it)}</text></g>')
            k += 1
        y += 50
    H = y - 12 + PAD
    bg = (f'<defs>{grad("bd", C, V, M, O)}<radialGradient id="gl"><stop offset="0" stop-color="{V}" stop-opacity=".3"/><stop offset="1" stop-color="{V}" stop-opacity="0"/></radialGradient>'
          f'<clipPath id="win"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>'
          f'<g clip-path="url(#win)"><rect width="{W}" height="{H}" fill="#0c0919"/><circle cx="{W/2}" cy="{H}" r="320" fill="url(#gl)"/></g>'
          f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="18" fill="none" stroke="url(#bd)" stroke-opacity=".5" stroke-width="1.5"/>')
    write("ai-stack.svg", svg(W, H, bg + "".join(out), ".pill{animation:in .6s ease-out both}@keyframes in{from{opacity:0;transform:translateY(10px)}}"))

# ============================== PROJETS ==============================
def card(name, ic, cat, c1, c2, title_, desc, tags):
    W, H = 480, 270
    tlines = textwrap.wrap(title_, 34)
    dlines = textwrap.wrap(desc, 58)[:3]
    y = 112
    tt = "".join(f'<text x="26" y="{y+i*26}" font-size="21" font-weight="800" fill="{TXT}">{esc(l)}</text>' for i, l in enumerate(tlines))
    y = y + (len(tlines) - 1) * 26 + 30
    dd = "".join(f'<text x="26" y="{y+i*20}" font-size="13.5" fill="{MUTED}">{esc(l)}</text>' for i, l in enumerate(dlines))
    tg, x = [], 26
    for t in tags:
        w = tw(t, 12, .62) + 22
        tg.append(f'<rect x="{x:.0f}" y="{H-50}" width="{w:.0f}" height="26" rx="8" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".1"/>'
                  f'<text class="mono" x="{x+11:.0f}" y="{H-32}" font-size="12" fill="{TXT}">{esc(t)}</text>')
        x += w + 8
    body = f'''<defs>{grad("g", c1, c2, anim=True)}
<radialGradient id="gl"><stop offset="0" stop-color="{c1}" stop-opacity=".45"/><stop offset="1" stop-color="{c1}" stop-opacity="0"/></radialGradient>
<clipPath id="win"><rect width="{W}" height="{H}" rx="20"/></clipPath></defs>
<g clip-path="url(#win)"><rect width="{W}" height="{H}" fill="{CARD}"/>
<circle class="gl" cx="{W-10}" cy="10" r="190" fill="url(#gl)"/>
<rect width="{W}" height="4" fill="url(#g)"/>
<rect x="24" y="26" width="50" height="50" rx="15" fill="{c1}" fill-opacity=".16" stroke="url(#g)" stroke-width="1.5"/>
{icon(ic, 36, 38, 26, c1)}
<text class="mono" x="88" y="47" font-size="11.5" letter-spacing="1.4" font-weight="700" fill="{c1}">{esc(cat)}</text>
<text class="mono" x="88" y="66" font-size="12" fill="{MUTED}">github.com/NdiayeAmanatou</text>
<circle cx="{W-44}" cy="51" r="20" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".12"/>
<g class="ar">{icon("arrow", W-54, 41, 20, TXT, 2.2)}</g>
{tt}{dd}{"".join(tg)}</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="20" fill="none" stroke="url(#g)" stroke-opacity=".55" stroke-width="1.5"/>'''
    style = '''.gl{transform-box:fill-box;transform-origin:center;animation:gl 5s ease-in-out infinite}@keyframes gl{50%{transform:scale(1.25);opacity:.7}}
.ar{animation:ar 1.8s ease-in-out infinite}@keyframes ar{50%{transform:translateX(4px)}}'''
    write(f"card-{name}.svg", svg(W, H, body, style))

# ============================== FOOTER ==============================
def footer():
    W, H = 1200, 220
    body = f'''<defs>{grad("w1", V, M, O)}{grad("w2", C, V, M)}{grad("t", V, M, O, anim=True)}</defs>
<text x="{W/2}" y="64" font-size="26" font-weight="800" fill="url(#t)" text-anchor="middle">Merci pour votre visite ✦</text>
<text class="mono" x="{W/2}" y="98" font-size="15" fill="{MUTED}" text-anchor="middle">« Transformer les connaissances en solutions concrètes à impact positif. »</text>
<g class="w a"><path d="M0 170 Q150 130 300 170 T600 170 T900 170 T1200 170 T1500 170 T1800 170 T2100 170 T2400 170 V220 H0Z" fill="url(#w2)" opacity=".35"/></g>
<g class="w b"><path d="M0 185 Q150 150 300 185 T600 185 T900 185 T1200 185 T1500 185 T1800 185 T2100 185 T2400 185 V220 H0Z" fill="url(#w1)" opacity=".75"/></g>'''
    style = '''.w{animation:wave 9s linear infinite}.b{animation-duration:6s;animation-direction:reverse}
@keyframes wave{from{transform:translateX(0)}to{transform:translateX(-600px)}}'''
    write("footer.svg", svg(W, H, body, style))

header()
button("portfolio", "Mon Portfolio", "globe", V, M, O, primary=True)
button("cv", "Mon CV", "download", G, C)
button("linkedin", "LinkedIn", "linkedin", C, B)
button("email", "Me contacter", "mail", M, O)
button("repos", "Voir tous mes dépôts", "folder", V, C)
for n, num, lab in [("about", "01", "À propos"), ("journey", "02", "Parcours"), ("stack", "03", "Arsenal technique"),
                    ("projects", "04", "Projets à la une"), ("stats", "05", "Activité GitHub")]:
    title(n, num, lab)
terminal(); focus(); timeline(); ai_stack(); footer()
card("rag", "shield", "IA & LLM", O, M, "Pipeline RAG — Cybersécurité",
     "Pipeline RAG de bout en bout : ingestion de PDF, nettoyage, chunking optimisé, embeddings et base vectorielle ChromaDB pour la recherche sémantique.",
     ["Python", "LLM", "RAG", "ChromaDB"])
card("business", "briefcase", "IA & LLM", M, O, "AI Business Assistant",
     "Prompt engineering appliqué à l'analyse des retours clients : anatomie d'un prompt et benchmark zero-shot, one-shot et few-shot.",
     ["LLM", "Prompting", "NLP"])
card("energy", "zap", "DEEP LEARNING", V, M, "Prédiction de consommation énergétique",
     "Réseau de neurones TensorFlow/Keras qui prédit la consommation d'énergie d'un bâtiment intelligent à partir de capteurs IoT.",
     ["TensorFlow", "Keras", "IoT"])
card("iot", "activity", "MACHINE LEARNING", M, V, "Classification de capteurs IoT",
     "Modèle KNN qui prédit l'état d'un capteur : standardisation, split stratifié, matrice de confusion et export du modèle.",
     ["scikit-learn", "KNN", "Pandas"])
card("aws", "cloud", "BACK-END & CLOUD", C, V, "API Spring Boot sur AWS",
     "API REST en Java / Spring Boot avec Maven, structurée de façon professionnelle pour un déploiement dans le cloud AWS.",
     ["Java", "Spring Boot", "AWS"])
card("web", "layout", "WEB", C, B, "AI Workspace — Dashboard",
     "Tableau de bord web responsive pour un espace de travail IA : composants interactifs en HTML, CSS et JavaScript.",
     ["HTML", "CSS", "JavaScript"])
print(sorted(os.listdir(OUT)))
