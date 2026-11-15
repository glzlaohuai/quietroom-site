#!/usr/bin/env python3
"""Generate the static QuietRoom site (English at /, Simplified Chinese at /zh/).

Usage: python3 tools/build.py
All copy lives here so both languages stay in step. No analytics, cookies or third-party requests.
"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = 'https://quietroom.hiimobapps.cn/'
EMAIL = '494763134@qq.com'
UPDATED = '2026-11-15'
# Set once the app is publicly available; until then the button says "coming soon".
APP_STORE_URL = None

T = {
 'en': dict(
  lang='en', locale='en_US', prefix='', other='zh/', other_label='中文', name='QuietRoom',
  nav=('Features', 'Support', 'Privacy'),
  title='QuietRoom: Spatial nature sounds for focus and rest',
  desc='Arrange rain, forest, water and fire sounds around you in 3D. 36 bundled nature sounds, offline playback, sleep timer and optional head tracking on iPhone.',
  hero_kicker='For iPhone · iOS 18 or later',
  hero_title='A little quiet, right here.',
  hero_body='QuietRoom places nature sounds around you: rain on the window to your left, a stream ahead, a fire just behind. Put on headphones, start listening, and shape the room until it feels right.',
  cta_soon='Coming soon on the App Store', cta='Download on the App Store', cta_support='Get support',
  shots=[('home-playing', 'Rainy study playing, with sound sources around a 3D listener'), ('source-edit', 'Editing direction, height and distance of a sound'), ('rooms', 'Curated rooms and saved rooms')],
  features_title='Everything a quiet room needs',
  features=[
   ('Sounds in real space', 'Drag each spatial source around a 3D listener, or set direction, height and distance precisely. Wide ambience stays steady around you.'),
   ('36 natural sounds', 'Rain, thunder, birds, streams, waves, wind, insects, footsteps and fire, with recordings that vary naturally so the room never feels like a short loop.'),
   ('Occasional sounds, your pace', 'Thunder, birdsong, drips and footsteps arrive now and then. Choose rare, normal or frequent for each one.'),
   ('Listen before you add', 'Preview any sound in the library, including Pro sounds, for as long as you like before adding it to your room.'),
   ('Head tracking', 'With compatible headphones, spatial sources stay put as you turn your head. Regular headphones still give fixed spatial sound.'),
   ('Offline, private, calm', 'No account, no ads, no analytics. Sounds are bundled, so listening, editing and saving work without a connection. A sleep timer fades out gently.'),
  ],
  pricing_title='Free to start. One purchase for everything.',
  free_title='Free', free_items=['The complete Rainy study room', 'Three sounds, up to three layers', 'Spatial editing and head tracking', 'Offline and background playback, sleep timer', 'One saved room', 'Preview every sound'],
  pro_title='QuietRoom Pro', pro_note='One-time purchase · no subscription',
  pro_items=['Forest camp and Seaside cabin rooms', 'All 36 sounds', 'Up to six layers per room', 'Up to twenty saved rooms'],
  pro_price='Price is shown by the App Store in your region.',
  foot_rights='© 2026 hiimobapps', foot_contact='Contact',
  privacy_title='Privacy Policy', privacy_desc='QuietRoom keeps your rooms on your device. No accounts, advertising, tracking or analytics.',
  support_title='Support', support_desc='Help with QuietRoom: purchases, head tracking, sound previews, timers and contact details.',
 ),
 'zh': dict(
  lang='zh-CN', locale='zh_CN', prefix='../', other='../', other_label='English', name='静室 QuietRoom',
  nav=('功能', '支持', '隐私'),
  title='静室 QuietRoom：可摆放的空间自然声音',
  desc='把雨声、森林、水声和壁炉声摆放在你身边。36 种随 App 安装的自然声音，离线播放、定时渐弱，兼容耳机可开启头部追踪。',
  hero_kicker='适用于 iPhone · iOS 18 或更高版本',
  hero_title='给此刻留一点安静。',
  hero_body='静室把自然声音摆放在你身边：左侧窗上的雨，前方的溪流，身后不远处的炉火。戴上耳机，开始聆听，再把房间调整到最舒服的样子。',
  cta_soon='即将登陆 App Store', cta='在 App Store 下载', cta_support='获取支持',
  shots=[('home-playing', '雨夜书房正在播放，声源分布在三维聆听者周围'), ('source-edit', '调整声音的方向、仰角和距离'), ('rooms', '精选房间与我的房间')],
  features_title='一个安静房间需要的一切',
  features=[
   ('声音有真实位置', '在三维聆听者周围拖动声源，或精确设置方向、仰角和距离。宽阔的环境底声稳定地包围着你。'),
   ('36 种自然声音', '雨、雷、鸟鸣、溪流、海浪、风、虫鸣、脚步和炉火。录音片段自然轮换，听久了也不像短循环。'),
   ('偶发声音，按你的节奏', '雷声、鸟鸣、水滴和脚步会不时出现。每一种都可以选择偶尔、适中或频繁。'),
   ('先试听，再添加', '声音库里的每一种声音都能试听，包括 Pro 声音，想听多久都可以，满意再加入房间。'),
   ('头部追踪', '使用兼容耳机时，转头后定位声音仍停留在原处。普通耳机也能听到固定的空间效果。'),
   ('离线、私密、安静', '无账户、无广告、无统计分析。声音随 App 安装，聆听、编辑和保存都不需要网络。定时结束时轻轻渐弱。'),
  ],
  pricing_title='免费开始，一次购买解锁全部。',
  free_title='免费', free_items=['完整的雨夜书房', '三种声音，最多三层', '空间摆放与头部追踪', '离线与后台播放、定时', '保存一个房间', '所有声音都可试听'],
  pro_title='静室 Pro', pro_note='一次性购买 · 不是订阅',
  pro_items=['森林营地与海边小屋', '全部 36 种声音', '每个房间最多六层', '最多保存二十个房间'],
  pro_price='价格以你所在地区 App Store 显示为准。',
  foot_rights='© 2026 hiimobapps', foot_contact='联系',
  privacy_title='隐私政策', privacy_desc='静室把你的房间留在设备上。无账户、广告、追踪或统计分析。',
  support_title='支持', support_desc='静室帮助：购买与恢复、头部追踪、试听、定时及联系方式。',
 ),
}

PRIVACY = {
 'en': [
  ('Summary', ['QuietRoom is published by hiimobapps. It has no accounts, advertising, tracking or third-party analytics, and there is no QuietRoom server. The app does not collect personal data.']),
  ('Data on your device', ['Sounds are bundled with the app. Your rooms, settings and the latest valid backup are stored only in the app’s local container on your iPhone. There is no cloud sync. Device backups you make through Apple may include this app data according to your own settings.', 'Deleting the app removes its rooms from your device.']),
  ('Head tracking and motion', ['When you turn on head tracking with compatible headphones, orientation is processed locally by Apple’s audio system. QuietRoom does not record, store or upload head-pose or motion history. Declining Motion access does not prevent ordinary playback.']),
  ('Purchases', ['Purchases and restores are handled by Apple through StoreKit under Apple’s terms. QuietRoom receives only the verified status of your purchase and never sees payment-card details. Restoring on a new installation needs an internet connection.']),
  ('Permissions', ['QuietRoom does not request microphone, location, contacts, photos, health or advertising-tracking access.']),
  ('Children', ['QuietRoom does not knowingly collect information from anyone, including children.']),
  ('Contacting us', ['If you email us, we use your message only to reply, and you can ask us to delete it at any time. Contact: ' + EMAIL + '.']),
  ('Changes', ['If this policy changes, the updated version will be posted on this page with a new date.']),
 ],
 'zh': [
  ('概要', ['静室由 hiimobapps 发布。静室不设账户，不接入广告、追踪或第三方统计分析，也没有静室服务器。App 不收集个人数据。']),
  ('保存在设备上的数据', ['声音随 App 安装。你的房间、设置和最近一次有效备份只保存在 iPhone 上的 App 本地容器中，没有云同步。你通过 Apple 进行的设备备份可能会按你的设置包含这些数据。', '删除 App 会移除设备上的房间。']),
  ('头部追踪与运动数据', ['在兼容耳机上开启头部追踪时，方向由 Apple 音频系统在本地处理。静室不记录、保存或上传头部姿态和运动轨迹。拒绝运动权限不影响正常播放。']),
  ('购买', ['购买与恢复购买由 Apple 通过 StoreKit 按 Apple 条款处理。静室只获得已验证的购买状态，不接触支付卡信息。在新安装上恢复购买需要联网。']),
  ('权限', ['静室不请求麦克风、定位、通讯录、照片、健康或广告追踪权限。']),
  ('儿童', ['静室不会有意收集任何人（包括儿童）的信息。']),
  ('联系我们', ['如果你发邮件给我们，我们只用它来回复你，你可以随时要求删除。联系邮箱：' + EMAIL + '。']),
  ('政策变更', ['本政策如有更新，会在此页面发布新版本并更新日期。']),
 ],
}

FAQ = {
 'en': [
  ('How do I restore my Pro purchase?', 'Open Settings (the ··· button) or the Pro page and tap Restore purchases. Use the same Apple Account you bought with. A new installation needs an internet connection the first time.'),
  ('Is Pro a subscription?', 'No. QuietRoom Pro is a one-time, non-consumable purchase. Refunds follow Apple’s policies.'),
  ('Head tracking says it is unavailable.', 'Head tracking needs headphones that support it, spatial audio enabled for the current output, and Motion access for QuietRoom. It starts while a room is playing. Regular headphones still give fixed spatial sound, and speakers give basic playback.'),
  ('How long does a sound preview last?', 'As long as you like. A preview plays until you tap Stop, close the sound library or leave the app. Any sound can be previewed, including Pro sounds. A playing room lowers its volume during the preview.'),
  ('Thunder or birds come too rarely, or too often.', 'Tap the sound in your room and choose Rare, Normal or Frequent under How often. Footsteps also offer occasional steps or a continuous walk.'),
  ('Does QuietRoom play in the background?', 'Yes. Playback continues on the lock screen and in the background, with lock-screen controls. Turn on Mix with other audio in Settings to play alongside other apps.'),
  ('How does the sleep timer work?', 'Choose 15, 30, 60 or 120 minutes. The room fades out over the last ten seconds and stops. Pausing manually turns the timer off.'),
  ('Where are my rooms stored? How do I delete them?', 'Only on your iPhone. Delete a room from Rooms → ··· → Delete, or delete the app to remove everything.'),
 ],
 'zh': [
  ('如何恢复 Pro 购买？', '打开设置（··· 按钮）或 Pro 页面，点击“恢复购买”。请使用购买时的 Apple 账户。新安装首次恢复需要联网。'),
  ('Pro 是订阅吗？', '不是。静室 Pro 是一次性的非消耗型购买。退款按 Apple 政策处理。'),
  ('头部追踪显示不可用。', '头部追踪需要支持该功能的耳机、当前输出已开启空间音频，并允许静室使用运动权限。它在房间播放时启动。普通耳机仍可听到固定空间效果，扬声器提供基础播放。'),
  ('试听能听多久？', '想听多久都可以。试听会一直播放，直到你点“停止”、关闭声音库或离开 App。所有声音都能试听，包括 Pro 声音。试听时正在播放的房间会暂时降低音量。'),
  ('雷声或鸟鸣太少或太多。', '在房间里点这个声音，在“出现频率”中选择偶尔、适中或频繁。脚步还可以选择偶发脚步或持续散步。'),
  ('可以后台播放吗？', '可以。锁屏和后台都会继续播放，并提供锁屏控制。在设置中打开“与其他音频同时播放”即可和其他 App 一起播放。'),
  ('定时是怎样工作的？', '可选择 15、30、60 或 120 分钟。最后十秒轻轻渐弱后停止。手动暂停会关闭定时。'),
  ('房间保存在哪里？如何删除？', '只保存在你的 iPhone 上。在“房间 → ··· → 删除”中删除单个房间，删除 App 会移除全部数据。'),
 ],
}
SUPPORT_TEXT = {
 'en': dict(intro='We read every message. Write to us and include your iPhone model, iOS version and what you were doing when the problem happened.', email_label='Email', reqs_title='Requirements', reqs='iPhone with iOS 18 or later. Head tracking requires compatible headphones and Motion access.', faq_title='Frequently asked questions', safety='Digital volume is not a measure of headphone sound pressure. Please listen at a comfortable level.'),
 'zh': dict(intro='每一封邮件我们都会阅读。来信时请附上 iPhone 型号、iOS 版本，以及出现问题时你在做什么。', email_label='邮箱', reqs_title='系统要求', reqs='iOS 18 或更高版本的 iPhone。头部追踪需要兼容耳机和运动权限。', faq_title='常见问题', safety='数字音量不代表耳机的实际声压，请以舒适的音量聆听。'),
}

e = html.escape


def head(t, page, title, desc):
    path = {'index': '', 'privacy': 'privacy.html', 'support': 'support.html'}[page]
    en_url, zh_url = BASE + path, BASE + 'zh/' + path
    url = en_url if t['lang'] == 'en' else zh_url
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', '@id': BASE + '#website', 'name': 'QuietRoom', 'url': BASE, 'inLanguage': ['en', 'zh-CN']},
        {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': title, 'description': desc, 'inLanguage': t['lang'], 'isPartOf': {'@id': BASE + '#website'}}]}
    if page == 'index':
        ld['@graph'].append({'@type': 'MobileApplication', 'name': 'QuietRoom', 'operatingSystem': 'iOS 18.0', 'applicationCategory': 'MusicApplication', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'publisher': {'@type': 'Organization', 'name': 'hiimobapps'}})
    p = t['prefix']
    return f'''<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="zh-CN" href="{zh_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<link rel="icon" href="{p}assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{p}assets/icon.png">
<meta name="theme-color" content="#F4F2EB" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#101713" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="QuietRoom">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:image" content="{BASE}assets/icon.png">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{p}assets/styles.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header class="bar"><div class="wrap bar-in">
<a class="brand" href="./"><img src="{p}assets/icon.png" alt="" width="32" height="32"><span>{e(t['name'])}</span></a>
<nav><a href="./#features">{t['nav'][0]}</a><a href="{local(t, 'support.html')}">{t['nav'][1]}</a><a href="{local(t, 'privacy.html')}">{t['nav'][2]}</a><a class="lang" href="{t['other']}{'' if page == 'index' else path}" hreflang="{'zh-CN' if t['lang'] == 'en' else 'en'}">{t['other_label']}</a></nav>
</div></header>
'''


def local(t, name):
    return name  # pages of one language share a folder


def foot(t):
    return f'''<footer class="foot"><div class="wrap foot-in">
<span>{t['foot_rights']}</span>
<span><a href="{local(t, 'privacy.html')}">{t['nav'][2]}</a> · <a href="{local(t, 'support.html')}">{t['nav'][1]}</a> · {t['foot_contact']}: <a href="mailto:{EMAIL}">{EMAIL}</a></span>
</div></footer>
</body>
</html>
'''


def cta(t):
    if APP_STORE_URL:
        return f'<a class="btn primary" href="{APP_STORE_URL}">{t["cta"]}</a>'
    return f'<span class="btn primary soon" aria-disabled="true">{t["cta_soon"]}</span>'


def index(t, code):
    shots = ''.join(f'<figure><img src="{t["prefix"] if code == "zh" else ""}assets/{code}/{n}.webp" alt="{e(a)}" width="552" height="1200" loading="lazy"><figcaption>{e(a)}</figcaption></figure>' for n, a in t['shots'])
    feats = ''.join(f'<article><h3>{e(h)}</h3><p>{e(b)}</p></article>' for h, b in t['features'])
    li = lambda xs: ''.join(f'<li>{e(x)}</li>' for x in xs)
    return head(t, 'index', t['title'], t['desc']) + f'''<main>
<section class="hero"><div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker">{e(t['hero_kicker'])}</p>
<h1>{e(t['hero_title'])}</h1>
<p class="lead">{e(t['hero_body'])}</p>
<div class="actions">{cta(t)}<a class="btn" href="support.html">{t['cta_support']}</a></div>
</div>
<div class="hero-shot"><img src="{t['prefix'] if code == 'zh' else ''}assets/{code}/home-playing.webp" alt="{e(t['shots'][0][1])}" width="552" height="1200"></div>
</div></section>
<section id="features" class="wrap features"><h2>{e(t['features_title'])}</h2><div class="grid">{feats}</div></section>
<section class="wrap shots" aria-label="Screenshots">{shots}</section>
<section class="wrap pricing"><h2>{e(t['pricing_title'])}</h2><div class="plans">
<div class="plan"><h3>{e(t['free_title'])}</h3><ul>{li(t['free_items'])}</ul></div>
<div class="plan pro"><h3>{e(t['pro_title'])}</h3><p class="note">{e(t['pro_note'])}</p><ul>{li(t['pro_items'])}</ul><p class="fine">{e(t['pro_price'])}</p></div>
</div></section>
</main>
''' + foot(t)


def doc(t, code, page, title, desc, body):
    return head(t, page, title + ' | QuietRoom', desc) + f'<main class="wrap doc"><h1>{e(title)}</h1>{body}</main>\n' + foot(t)


def privacy(t, code):
    upd = ('Last updated: ' if code == 'en' else '最后更新：') + UPDATED
    body = f'<p class="sub">{upd}</p>' + ''.join(f'<h2>{e(h)}</h2>' + ''.join(f'<p>{e(x)}</p>' for x in ps) for h, ps in PRIVACY[code])
    body = body.replace(e(EMAIL), f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
    return doc(t, code, 'privacy', t['privacy_title'], t['privacy_desc'], body)


def support(t, code):
    s = SUPPORT_TEXT[code]
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ[code])
    body = f'''<p class="lead">{e(s['intro'])}</p>
<p class="contact">{s['email_label']}: <a href="mailto:{EMAIL}?subject=QuietRoom">{EMAIL}</a></p>
<h2>{e(s['faq_title'])}</h2>{faq}
<h2>{e(s['reqs_title'])}</h2><p>{e(s['reqs'])}</p>
<p class="fine">{e(s['safety'])}</p>'''
    return doc(t, code, 'support', t['support_title'], t['support_desc'], body)


def main():
    for code, t in T.items():
        out = ROOT if code == 'en' else ROOT / 'zh'
        out.mkdir(exist_ok=True)
        (out / 'index.html').write_text(index(t, code))
        (out / 'privacy.html').write_text(privacy(t, code))
        (out / 'support.html').write_text(support(t, code))
    urls = ''
    for path in ['', 'privacy.html', 'support.html']:
        for loc in [BASE + path, BASE + 'zh/' + path]:
            urls += f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{UPDATED}</lastmod>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE + path}" />
    <xhtml:link rel="alternate" hreflang="zh-CN" href="{BASE + 'zh/' + path}" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE + path}" />
  </url>
'''
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {BASE}sitemap.xml\n')
    (ROOT / 'CNAME').write_text('quietroom.hiimobapps.cn\n')
    (ROOT / '.nojekyll').write_text('')
    print('built', sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*.html')))


if __name__ == '__main__':
    main()
