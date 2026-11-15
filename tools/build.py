#!/usr/bin/env python3
"""Generate the static QuietRoom site in every supported language.

Usage: python3 tools/build.py
Copy lives in tools/i18n/<lang>.json (one file per language, same structure as en.json).
English is served at /, other languages at /<slug>/. No analytics, cookies or third-party requests.
"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
I18N = ROOT / 'tools' / 'i18n'
BASE = 'https://quietroom.hiimobapps.cn/'
EMAIL = '494763134@qq.com'
UPDATED = '2026-11-15'
# Set once the app is publicly available; until then the button says "coming soon".
APP_STORE_URL = None
# Language file -> URL folder. Same set as the app's localizations.
LANGS = {'en': '', 'zh-Hans': 'zh', 'zh-Hant': 'zh-hant', 'ja': 'ja', 'ko': 'ko', 'de': 'de', 'fr': 'fr', 'es': 'es',
         'it': 'it', 'pt-BR': 'pt-br', 'ru': 'ru', 'nl': 'nl', 'tr': 'tr', 'th': 'th', 'id': 'id'}
SHOTS = ['home-playing', 'library', 'source-edit', 'rooms']
PAGES = {'index': '', 'privacy': 'privacy.html', 'support': 'support.html'}
e = html.escape
CURRENT, LAZY = ' aria-current="true"', ' loading="lazy"'


def load():
    out = {}
    for code, slug in LANGS.items():
        t = json.loads((I18N / f'{code}.json').read_text())
        t['code'], t['slug'] = code, slug
        t['prefix'] = '../' if slug else ''          # path from a page to the site root
        t['assets'] = slug or 'en'                    # screenshot folder
        out[code] = t
    return out


def url(t, page):
    return BASE + (t['slug'] + '/' if t['slug'] else '') + PAGES[page]


def head(t, all_t, page, title, desc):
    alternates = ''.join(f'<link rel="alternate" hreflang="{o["meta"]["lang"]}" href="{url(o, page)}">\n' for o in all_t.values())
    langs = ''.join(
        f'<li><a href="{t["prefix"]}{o["slug"] + "/" if o["slug"] else ""}{PAGES[page]}" hreflang="{o["meta"]["lang"]}" lang="{o["meta"]["lang"]}"'
        f'{CURRENT if o is t else ""}>{e(o["meta"]["label"])}</a></li>' for o in all_t.values())
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', '@id': BASE + '#website', 'name': 'QuietRoom', 'url': BASE, 'inLanguage': [o['meta']['lang'] for o in all_t.values()]},
        {'@type': 'WebPage', '@id': url(t, page) + '#webpage', 'url': url(t, page), 'name': title, 'description': desc, 'inLanguage': t['meta']['lang'], 'isPartOf': {'@id': BASE + '#website'}}]}
    if page == 'index':
        ld['@graph'].append({'@type': 'MobileApplication', 'name': 'QuietRoom', 'operatingSystem': 'iOS 18.0', 'applicationCategory': 'MusicApplication', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'publisher': {'@type': 'Organization', 'name': 'hiimobapps'}})
    p = t['prefix']
    return f'''<!doctype html>
<html lang="{t['meta']['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url(t, page)}">
{alternates}<link rel="alternate" hreflang="x-default" href="{url(all_t['en'], page)}">
<link rel="icon" href="{p}assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{p}assets/icon.png">
<meta name="theme-color" content="#F4F2EB" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#101713" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="QuietRoom">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url(t, page)}">
<meta property="og:locale" content="{t['meta']['locale']}">
<meta property="og:image" content="{BASE}assets/icon.png">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{p}assets/styles.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header class="bar"><div class="wrap bar-in">
<a class="brand" href="./"><img src="{p}assets/icon.png" alt="" width="32" height="32"><span>{e(t['name'])}</span></a>
<nav><a href="./#features">{e(t['nav'][0])}</a><a href="support.html">{e(t['nav'][1])}</a><a href="privacy.html">{e(t['nav'][2])}</a>
<details class="langs"><summary aria-label="{e(t['language_label'])}">{e(t['meta']['label'])}</summary><ul>{langs}</ul></details></nav>
</div></header>
'''


def foot(t):
    return f'''<footer class="foot"><div class="wrap foot-in">
<span>{e(t['foot_rights'])}</span>
<span><a href="privacy.html">{e(t['nav'][2])}</a> · <a href="support.html">{e(t['nav'][1])}</a> · {e(t['foot_contact'])}: <a href="mailto:{EMAIL}">{EMAIL}</a></span>
</div></footer>
</body>
</html>
'''


def cta(t):
    if APP_STORE_URL:
        return f'<a class="btn primary" href="{APP_STORE_URL}">{e(t["cta"])}</a>'
    return f'<span class="btn primary soon" aria-disabled="true">{e(t["cta_soon"])}</span>'


def shot(t, name, lazy=True):
    alt = e(t['shots'][name])
    return f'<img src="{t["prefix"]}assets/{t["assets"]}/{name}.webp" alt="{alt}" width="552" height="1200"{LAZY if lazy else ""}>'


def index(t, all_t):
    shots = ''.join(f'<figure>{shot(t, n)}<figcaption>{e(t["shots"][n])}</figcaption></figure>' for n in SHOTS[1:])
    feats = ''.join(f'<article><h3>{e(h)}</h3><p>{e(b)}</p></article>' for h, b in t['features'])
    li = lambda xs: ''.join(f'<li>{e(x)}</li>' for x in xs)
    return head(t, all_t, 'index', t['title'], t['desc']) + f'''<main>
<section class="hero"><div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker">{e(t['hero_kicker'])}</p>
<h1>{e(t['hero_title'])}</h1>
<p class="lead">{e(t['hero_body'])}</p>
<div class="actions">{cta(t)}<a class="btn" href="support.html">{e(t['cta_support'])}</a></div>
</div>
<div class="hero-shot">{shot(t, SHOTS[0], lazy=False)}</div>
</div></section>
<section id="features" class="wrap features"><h2>{e(t['features_title'])}</h2><div class="grid">{feats}</div></section>
<section class="wrap shots" aria-label="{e(t['screenshots_label'])}">{shots}</section>
<section class="wrap pricing"><h2>{e(t['pricing_title'])}</h2><div class="plans">
<div class="plan"><h3>{e(t['free_title'])}</h3><ul>{li(t['free_items'])}</ul></div>
<div class="plan pro"><h3>{e(t['pro_title'])}</h3><p class="note">{e(t['pro_note'])}</p><ul>{li(t['pro_items'])}</ul><p class="fine">{e(t['pro_price'])}</p></div>
</div></section>
</main>
''' + foot(t)


def doc(t, all_t, page, title, desc, body):
    return head(t, all_t, page, title + ' | QuietRoom', desc) + f'<main class="wrap doc"><h1>{e(title)}</h1>{body}</main>\n' + foot(t)


def privacy(t, all_t):
    mail = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    body = f'<p class="sub">{e(t["updated_label"])} {UPDATED}</p>' + ''.join(
        f'<h2>{e(h)}</h2>' + ''.join(f'<p>{e(x).replace("{email}", mail)}</p>' for x in ps) for h, ps in t['privacy'])
    return doc(t, all_t, 'privacy', t['privacy_title'], t['privacy_desc'], body)


def support(t, all_t):
    s = t['support']
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in t['faq'])
    body = f'''<p class="lead">{e(s['intro'])}</p>
<p class="contact">{e(s['email_label'])}: <a href="mailto:{EMAIL}?subject=QuietRoom">{EMAIL}</a></p>
<h2>{e(s['faq_title'])}</h2>{faq}
<h2>{e(s['reqs_title'])}</h2><p>{e(s['reqs'])}</p>
<p class="fine">{e(s['safety'])}</p>'''
    return doc(t, all_t, 'support', t['support_title'], t['support_desc'], body)


def main():
    all_t = load()
    for t in all_t.values():
        out = ROOT / t['slug'] if t['slug'] else ROOT
        out.mkdir(exist_ok=True)
        (out / 'index.html').write_text(index(t, all_t))
        (out / 'privacy.html').write_text(privacy(t, all_t))
        (out / 'support.html').write_text(support(t, all_t))
    urls = ''
    for page in PAGES:
        links = ''.join(f'    <xhtml:link rel="alternate" hreflang="{o["meta"]["lang"]}" href="{url(o, page)}" />\n' for o in all_t.values())
        links += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url(all_t["en"], page)}" />\n'
        for t in all_t.values():
            urls += f'  <url>\n    <loc>{url(t, page)}</loc>\n    <lastmod>{UPDATED}</lastmod>\n{links}  </url>\n'
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {BASE}sitemap.xml\n')
    (ROOT / 'CNAME').write_text('quietroom.hiimobapps.cn')
    (ROOT / '.nojekyll').write_text('')
    print('built', len(list(ROOT.rglob('*.html'))), 'pages in', len(all_t), 'languages')


if __name__ == '__main__':
    main()
