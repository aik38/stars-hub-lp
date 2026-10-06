#!/usr/bin/env python3
"""Build the static site; preserve approved metadata and legal source verbatim."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = '5202d303876cfca3b6205ef61a1e07a3648e6947'
VERSION = '20261006-operations'
LINE = 'https://lin.ee/X0mxy9O'
EMAIL = 'm-asakura@killerword.info'
ROUTES = ['index.html', 'contact-center/index.html', 'pricing/index.html', 'reputation/index.html', 'contact/index.html', 'privacy/index.html', 'legal/index.html', '404.html']

def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT, text=True)

def brand(prefix):
    return f'<a class="brand" href="{prefix}" aria-label="スターズハブ トップ"><span class="brand-symbol" aria-hidden="true">✳</span><span><strong>STARS HUB</strong><small>スターズハブ</small></span></a>'

def arrow():
    return '<span class="arrow" aria-hidden="true">↗</span>'

def button(href, text='導入について相談する', style='button-primary', external=False):
    attr = ' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a class="button {style}" href="{href}"{attr}>{text}{arrow()}</a>'

def line_link():
    return f'<a class="text-link" href="{LINE}" target="_blank" rel="noopener noreferrer">LINEで相談{arrow()}</a>'

def actions(prefix):
    return f'<div class="actions">{button(prefix+"contact/")}{line_link()}</div>'

def header(prefix, page):
    links = [('contact-center/', '予約受付'), ('pricing/', '料金'), ('reputation/', '店舗運営支援')]
    nav = ''.join(f'<a href="{prefix}{p}"'+(' aria-current="page"' if page.startswith(p) else '')+f'>{label}</a>' for p,label in links)
    return f'''<a class="skip-link" href="#main">本文へ移動</a>
<header class="site-header"><div class="container header-inner">{brand(prefix)}
<button class="menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="メニューを開く"><span></span><span></span><span class="menu-label">MENU</span></button>
<nav id="site-nav" class="site-nav" aria-label="メインメニュー">{nav}{button(prefix+'contact/')}<a class="nav-line" href="{LINE}" target="_blank" rel="noopener noreferrer">LINEで相談{arrow()}</a></nav></div></header>'''

def footer(prefix, page):
    mobile = '' if page == 'contact/index.html' else f'<div class="mobile-cta" hidden>{button(prefix+"contact/")}{line_link()}</div>'
    return f'''<footer class="site-footer"><div class="container"><div class="footer-top">{brand(prefix)}<p>店舗の受付を支え、<br>現場の時間をつくる。</p></div>
<nav class="footer-nav" aria-label="フッターメニュー"><div><strong>サービス</strong><a href="{prefix}contact-center/">予約受付・カスタマーサポート</a><a href="{prefix}pricing/">料金・案件の数え方</a><a href="{prefix}reputation/#growth">集客支援</a><a href="{prefix}reputation/#risk">評判・リスク対策</a><a href="{prefix}#faq">よくある質問</a></div><div><strong>ご相談</strong><a href="{prefix}contact/">導入について相談する</a><a href="{LINE}" target="_blank" rel="noopener noreferrer">LINEで相談</a><a href="mailto:{EMAIL}">メールでお問い合わせ</a></div><div><strong>運営情報</strong><a href="{prefix}legal/">運営者情報</a><a href="{prefix}privacy/">プライバシーポリシー</a><a href="https://kuchikomi-stars.com/" target="_blank" rel="noopener noreferrer">クチコミスターズ{arrow()}</a></div></nav>
<div class="footer-word" aria-hidden="true">STARS HUB<span>✳</span></div><div class="footer-bottom"><span>© 2026 スターズハブ</span><span>予約受付・カスタマーサポート</span></div></div></footer>{mobile}'''

def cta(prefix, headline='いまの受付を、<br>任せるところから。'):
    return f'''<section class="consultation"><div class="container consultation-inner"><div><p class="eyebrow">導入のご相談</p><h2>{headline}</h2><p>現在の受付方法と、任せたい業務をお聞かせください。<br class="desktop-break">店舗に合う運用と料金をご案内します。</p></div><div class="consultation-actions">{button(prefix+'contact/')}{line_link()}<a class="email-link" href="mailto:{EMAIL}">メールでお問い合わせ</a></div></div></section>'''

def subhero(prefix, label, h1, description, tone=''):
    return f'''<section class="subhero {tone}"><div class="container"><p class="breadcrumb"><a href="{prefix}">トップ</a><span aria-hidden="true">／</span>{label}</p><div class="subhero-grid"><div><p class="eyebrow">{label}</p><h1>{h1}</h1></div><p class="subhero-description">{description}</p></div></div></section>'''

def section_heading(number, label, h2, intro=''):
    return f'<div class="section-heading"><p class="eyebrow"><span>{number}</span>{label}</p><h2>{h2}</h2>'+ (f'<p class="section-description">{intro}</p>' if intro else '')+'</div>'

def faq(items):
    return '<div class="faq-list">'+''.join(f'<details><summary>{q}<span aria-hidden="true"></span></summary><div class="faq-answer">{a}</div></details>' for q,a in items)+'</div>'

FAQ_ENV = ('現在の予約システムやLINEは使えますか？', '<p>現在店舗で利用しているLINE、集客サイト、Web予約、予約表などの受付環境を確認し、既存運用を活かした対応方法をご案内します。使用する管理画面や権限、店舗の運用方法に合わせて対応範囲を決めます。</p>')
FAQ_TIME = ('対応時間は決まっていますか？', '<p>対応時間は店舗の営業時間やご希望に合わせて個別に設定します。深夜・祝日の運用もご相談いただけます。</p>')
FAQ_MULTI = ('複数店舗でも利用できますか？', '<p>原則として1店舗を1契約・1運用単位とします。1屋号・1受付運用単位を1店舗の目安とし、複数店舗の場合は個別に設計・見積します。</p>')
FAQ_COUNT = ('電話やLINEの連絡回数で料金が増えますか？', '<p>原則として予約成立1件を1案件とし、連絡回数では数えません。予約に至らない問い合わせは0案件、同一予約の変更・キャンセルは追加カウントなしです。標準案件数を超えた場合は1案件3,300円（税込）です。</p>')

def onboarding(full=False):
    items = [('ヒアリング', '現在の受付方法、予約ルール、任せたい業務を確認します。'), ('受付フロー設計', '対応方法、連絡先、顧客情報の扱い、必要な権限や設定を整理します。'), ('運用確認', '予約表への反映、共有内容、店舗側の判断が必要な場合の連絡先を確認します。'), ('運用開始', '合意した受付フローに沿って、日々の対応を開始します。')]
    rows = ''.join(f'<li><span class="step-number">0{i}</span><h3>{h}</h3><p>{t}</p></li>' for i,(h,t) in enumerate(items,1))
    note = '予約受付・カスタマーサポートは、最短即日で導入準備を開始可能です。実際の運用開始日は、受付環境、権限設定、店舗ルール等に応じて個別にご案内します。'
    return f'<ol class="onboarding-list">{rows}</ol><p class="fine-print">{note}</p>'

def plan_table():
    plans=[('ベース','50','案件まで','165,000',''),('スタンダード','100','案件まで','297,000',''),('カスタム','150','案件〜','440,000','〜')]
    rows=''.join(f'<div class="plan-row"><h3>{n}</h3><p class="plan-volume"><strong>{v}</strong><span>{count}</span></p><p class="plan-price"><strong>{price}</strong><span>円{suffix}<small> / 月</small></span></p></div>' for n,v,count,price,suffix in plans)
    return f'<div class="plans" aria-label="月額プラン。すべて税込"><div class="plan-table-heading"><span>プラン</span><span>月間の受付量</span><span>月額・税込</span></div>{rows}</div>'

def price_notes():
    return '<p class="fine-print">表示価格はすべて税込です。原則として予約成立1件を1案件とします。1屋号・1受付運用単位を1店舗の目安とし、複数店舗は個別に設計・見積します。</p>'

def support_prices(kind):
    if kind=='content': rows=[('10件','27,500円〜'),('20件','52,800円〜'),('50件','126,500円〜'),('100件','242,000円〜')]
    elif kind=='profile': rows=[('標準 <small>600〜900字程度</small>','7,700円'),('ロング <small>ロング文章＋キャッチコピー3本</small>','11,000円')]
    else: rows=[('初回100件','9,900円'),('300件','29,700円'),('500件','49,500円'),('1,000件','88,000円')]
    return '<dl class="rate-list">'+''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a,b in rows)+'</dl>'

def industries():
    return '''<div class="industry-group"><h3>予約受付・カスタマーサポート</h3><ul class="industry-list"><li>アロマエステ</li><li>デリヘル</li><li>ホテヘル</li><li>ファッションヘルス</li><li>ソープ</li><li>その他予約型サービス</li></ul></div><div class="industry-group industry-secondary"><h3>集客支援・評判／リスク対策</h3><ul class="industry-list"><li>キャバクラ・ラウンジ</li><li>ガールズバー</li><li>ホストクラブ</li></ul></div>'''

def voices():
    pairs=[('予約ミス防止','メンズエステ / 2店舗','電話予約とLINE予約、さらにポータルサイトからのネット予約が混在し、ダブルブッキングが頻発していました。スターズハブに全てを一元管理してもらってからは、予約被りのミスが完全にゼロになりました。'), ('現場負担の軽減','店舗型サロン / 4店舗','これまでは施術中のスタッフが手を止めて電話に出ており、目の前のお客様に申し訳ない思いをしていました。受付窓口が完全に分離されたことで、接客に100%集中できるようになり、顧客満足度も向上しました。')]
    compact=[('顧客管理','キャバクラ / 3店舗','これまで手書きのメモやスタッフの頭の中にしかなかった『お客様の細かい要望や特徴』が、顧客履歴としてデータで正確に管理されるようになりました。'),('現場との連携','メンズエステ / 3店舗','店舗からセラピストへの連絡事項が的確で漏れがありません。細かいお客様の特徴や好みを事前に伝えてくれるため、セラピストからの『仕事がしやすい』という声が増え、離職率低下にも繋がっています。'),('対応品質','高級エステサロン / 1店舗','オペレーターの言葉遣いや電話対応が非常に丁寧で、来店されたお客様から『電話の対応がとても良かった』と褒められることが増えました。店舗の顔として安心して任せられます。'),('複数店舗運営','デリヘル / 5店舗','店舗が増えるにつれて本部の受付業務がパンク状態でしたが、カスタムプランで全店舗の窓口を一本化できました。オペレーションが安定したことで、さらなる店舗展開を加速できています。')]
    def quote(item):
        label,attr,text=item
        return f'<figure class="voice"><p class="voice-label">{label}</p><blockquote><p>{text}</p></blockquote><figcaption>{attr}</figcaption></figure>'
    return '''<figure class="voice-feature"><div class="voice-metric"><span>月間売上</span><strong>1.3<span>倍</span></strong><small>デリヘル / 2店舗</small></div><div><p class="voice-label">予約機会を逃しにくく</p><blockquote><p>ピーク帯（20時〜24時）の電話の取りこぼしが毎日のように発生していましたが、スターズハブに全件委託したことで取りこぼしがゼロに。結果として機会損失がなくなり、月間の売上が約1.3倍に伸びました。</p></blockquote><figcaption>デリヘル / 2店舗</figcaption></div></figure>'''+ '<div class="voice-pair">'+''.join(map(quote,pairs))+'</div><div class="voice-grid">'+''.join(map(quote,compact))+'</div>'

def home():
    p='./'
    return f'''<section class="hero"><div class="container hero-grid"><div class="hero-copy"><p class="eyebrow">店舗のための予約受付・カスタマーサポート</p><h1><span>すべての予約受付を、</span><span>ひとつに。</span></h1><p class="hero-description">問い合わせ対応から予約確定、現場への共有まで。<br class="desktop-break">日々の受付業務を、店舗に代わって運用します。</p>{actions(p)}<a class="hero-detail" href="./contact-center/">任せられる業務を見る<span aria-hidden="true">↓</span></a></div><div class="hero-visual"><img src="./assets/operations.svg" width="620" height="650" alt="" fetchpriority="high"><div class="visual-caption"><span>受付から、現場まで。</span><small>STARS HUB</small></div></div></div><div class="container hero-bottom"><span>予約受付</span><span>顧客情報・対応履歴</span><span>店舗・担当者への共有</span><a href="#services" aria-label="サービス紹介へ">SCROLL<span aria-hidden="true">↓</span></a></div></section>
<section class="section intro" id="services"><div class="container"><div class="intro-layout"><div>{section_heading('01','受付業務を任せる','受付は、任せる。<br>現場は、接客に集中する。')}</div><div class="intro-copy"><p>手を止めて、電話に出る。<br>接客の合間に、LINEを返す。<br>予約表を確認し、担当者へ連絡する。</p><p>その一連の業務を、スターズハブへ。<br>予約の入口から現場への引き継ぎまで、<br>店舗のルールに沿って対応します。</p></div></div><div class="benefits"><div><span>01</span><h3>予約の機会を逃しにくく。</h3><p>対応の遅れや取りこぼしを減らし、<br>問い合わせを予約につなげる。</p></div><div><span>02</span><h3>予約管理を、ひとつの運用に。</h3><p>窓口が違っても予約表へ反映し、<br>情報の行き違いを防ぐ。</p></div><div><span>03</span><h3>現場の時間を、接客へ。</h3><p>受付と連絡の負担を外部化し、<br>目の前のお客様へ集中する。</p></div></div></div></section>
<section class="section service-band" id="reception"><div class="container service-layout"><div>{section_heading('02','任せられる業務','予約が入る。<br>情報が整う。<br>現場へ届く。')}<p class="section-description">対応をひとつにつなげて、<br>日々の受付を運用します。</p><a class="text-link" href="./contact-center/">業務内容を詳しく見る{arrow()}</a></div><div class="service-ledger"><article><span>01</span><div><h3>問い合わせ・予約対応</h3><p>空き状況の確認、料金・コース案内、予約調整・確定。変更・キャンセルにも対応します。</p></div></article><article><span>02</span><div><h3>予約表・顧客情報への反映</h3><p>予約表・台帳を更新。顧客履歴、リピーター情報、注意事項・NG情報を確認・記録します。</p></div></article><article><span>03</span><div><h3>店舗・担当者への共有</h3><p>予約内容、変更点、必要な注意事項を、店舗ごとに決めた相手へ共有します。</p></div></article></div></div></section>
<section class="section trust"><div class="container trust-layout"><div class="trust-statement"><p class="eyebrow">店舗ごとに、運用を設計。</p><h2>いつもの環境で。<br>店舗のルールで。</h2><div class="trust-graphic" aria-hidden="true"><span>STARS</span><i></i><span>HUB</span></div></div><div class="trust-copy"><p class="eyebrow">03　任せるための運用設計</p><article><h3>今の受付環境を活かす</h3><p>電話・LINE・予約サイト・予約表など、現在の環境を確認。使っている仕組みに合わせて対応方法を設計します。</p></article><article><h3>判断と共有のルールを決める</h3><p>店舗側の判断が必要な場合の連絡先、対応権限、共有する内容を、導入時に確認します。</p></article><article><h3>顧客情報は店舗単位で扱う</h3><p>顧客情報・対応履歴・注意事項・NG情報は原則として店舗単位で管理し、合意した共有先へ伝えます。</p></article></div></div></section>
<section class="section voices" id="voices"><div class="container">{section_heading('04','お客様の声','任せた先に、<br>現場の変化がある。')}{voices()}</div></section>
<section class="section pricing-band" id="pricing"><div class="container"><div class="pricing-intro">{section_heading('05','予約受付の料金','任せる受付量で、選ぶ。')}<p>予約受付・顧客情報の確認と記録・現場共有。<br>一連の対応は、全プランに含まれます。</p></div>{plan_table()}<div class="fee-strip"><p><span>初期導入費 <small>導入キャンペーン</small></span><strong>11,000<small>円</small></strong><small>通常33,000円</small></p><p><span>標準案件数を超えた場合</span><strong>3,300<small>円 / 案件</small></strong></p></div>{price_notes()}<div class="pricing-more"><p>問い合わせの回数ではなく、<strong>予約成立1件＝1案件。</strong></p><a class="text-link" href="./pricing/">料金・案件の数え方を詳しく見る{arrow()}</a></div></div></section>
<section class="section industries" id="industries"><div class="container">{section_heading('06','対応業種','業種のルールに合わせて。','予約方法、連絡先、情報の扱い。店舗ごとの運用に合わせて対応します。')}{industries()}</div></section>
<section class="section support" id="support"><div class="container"><div class="support-heading"><p class="eyebrow">必要に応じて追加できる店舗運営支援</p><h2>受付の、その先も。</h2></div><a class="support-row" href="./reputation/#growth"><span>01</span><h3>集客支援</h3><p>媒体・求人コンテンツ制作、<br>プロフィール文章制作。</p>{arrow()}</a><a class="support-row" href="./reputation/#risk"><span>02</span><h3>評判・リスク対策</h3><p>掲示板対策と、<br>投稿モニタリング。</p>{arrow()}</a><div class="related-line"><p>Google口コミ獲得・運用の専門サービス</p><a href="https://kuchikomi-stars.com/" target="_blank" rel="noopener noreferrer">クチコミスターズ{arrow()}</a></div></div></section>
<section class="section onboarding" id="onboarding"><div class="container split-section">{section_heading('07','導入の流れ','確認してから、<br>受付をスタート。')}<div>{onboarding()}</div></div></section>
<section class="section faq-section" id="faq"><div class="container split-section">{section_heading('08','ご相談の前に','よくある質問')}<div>{faq([FAQ_ENV,FAQ_TIME,FAQ_MULTI,FAQ_COUNT])}<a class="text-link faq-more" href="./contact-center/#faq">予約受付について詳しく見る{arrow()}</a></div></div></section>{cta(p)}'''

def contact_center():
    p='../'
    rows = [('01','問い合わせ受付から予約確定まで','空き状況の確認、料金・コース案内、日程やコースの調整、予約確定まで対応します。','問い合わせ対応 ／ 空き状況確認 ／ 料金・コース案内 ／ 予約調整・確定'),('02','予約表・台帳へ、確定情報を反映','予約日時、コース、担当者などの必要な情報を、店舗の予約表・台帳へ反映します。','予約内容の入力 ／ 顧客情報の確認・記録'),('03','履歴や注意事項を確認する','顧客履歴、リピーター情報、過去の対応、注意事項・NG情報を各対応で確認・更新します。','顧客履歴 ／ 対応履歴 ／ リピーター情報 ／ 注意事項・NG情報'),('04','変更・キャンセルを運用へ反映','変更やキャンセルに対応し、予約表と共有情報を更新します。同一予約の変更・キャンセルは追加カウントしません。','変更・キャンセル対応 ／ 予約表の更新 ／ 関係者への連絡'),('05','必要な情報を、必要な相手へ','予約内容、変更点、必要な注意事項を、店舗・担当者など、合意した共有先へ伝えます。現在の連絡方法に合わせて運用します。','予約内容の共有 ／ 変更点・注意事項の共有')]
    work = ''.join(f'<article class="work-row"><span>{n}</span><h3>{h}</h3><div><p>{t}</p><p class="work-scope">{s}</p></div></article>' for n,h,t,s in rows)
    questions=[('どこまで任せられますか？','<p>問い合わせ受付、空き確認、料金・コース案内、予約調整・確定、変更・キャンセル、予約表・台帳への反映、店舗・担当者への共有に対応します。顧客履歴・注意事項・NG情報等は各対応で確認・更新します。具体的な対応方法は店舗のルールと利用環境に合わせて設計します。</p>'),FAQ_ENV,('電話以外の問い合わせにも対応できますか？','<p>電話・SMS・LINE・集客サイト・Web予約・メールなど、複数の受付窓口に対応します。集客サイトは外部の掲載・集客媒体経由、Web予約は自社サイトやオンライン予約システムから直接入る受付です。</p>'),FAQ_TIME,('今の電話番号は使えますか？','<p>店舗の既存番号からの転送、または新しい受付番号の用意のどちらにも対応します。ご希望と現在の電話環境に合わせて設計します。</p>'),('顧客情報や注意事項はどのように扱いますか？','<p>顧客情報、予約履歴、対応履歴、リピーター情報、注意事項、NG情報などは原則として店舗単位で扱います。必要な情報を各対応で確認・更新し、合意した共有先へ伝えます。保存期間や閲覧権限等は契約・初期導入時の運用設計で決めます。詳しくは<a href="../privacy/">プライバシーポリシー</a>をご確認ください。</p>'),FAQ_MULTI,('導入までどれくらいかかりますか？','<p>予約受付・カスタマーサポートは最短即日で導入準備を開始可能です。運用開始日は、受付環境、権限設定、店舗ルール等に応じて個別にご案内します。集客支援・評判／リスク対策は、内容確認後、最短即日着手可能です。</p>'),('相談時には何を伝えればよいですか？','<p>ご希望のサービスと、現在の受付方法・掲載媒体・困っていることをお聞かせください。予約受付の場合は、料金・コース、予約ルール、予約表、担当者への連絡方法等も確認します。分かる範囲で構いません。</p>')]
    return subhero(p,'予約受付・カスタマーサポート','受付の一連の業務を、<br>店舗に代わって。','問い合わせ対応から予約確定、顧客情報の確認、現場への共有まで。店舗ごとの運用に合わせて実際の業務を担います。','subhero-dark')+f'''<nav class="page-jump container" aria-label="ページ内メニュー"><a href="#scope">任せられる業務</a><a href="#environment">既存環境の活用</a><a href="#setup">導入の流れ</a><a href="#faq">よくある質問</a></nav><section class="section" id="scope"><div class="container">{section_heading('01','対応業務','受付から、引き継ぎまで。')}<div class="work-list">{work}</div></div></section>
<section class="section service-band" id="environment"><div class="container split-section">{section_heading('02','既存の受付環境','使い慣れた仕組みを、<br>運用の土台に。')}<div><p class="large-copy">現在の電話・LINE・予約サイト・予約表を確認し、店舗のルールに合わせて対応方法を設計します。</p><div class="channel-line"><span>電話</span><span>SMS</span><span>LINE</span><span>集客サイト</span><span>Web予約</span><span>メール</span></div><p>集客サイトは外部の掲載・集客媒体からの受付、Web予約は自社サイトやオンライン予約システムから直接入る受付です。</p><p>電話は既存番号からの転送と、新しい受付番号の用意のどちらにも対応します。管理画面や権限、予約ルール、連絡方法を確認して運用範囲を決めます。</p></div></div></section>
<section class="section"><div class="container policy-layout"><div>{section_heading('03','情報管理と判断','共有する情報。<br>任せる権限。')}<p class="section-description">安心して任せるためのルールを、<br>導入時に確認します。</p></div><div class="policy-list"><article><h3>顧客情報は店舗単位で管理</h3><p>顧客情報・対応履歴・注意事項・NG情報は原則として店舗単位で扱います。店舗をまたいだ共通ブラックリストとして管理するものではありません。</p></article><article><h3>共有先と閲覧権限を確認</h3><p>必要な情報は、合意した店舗・担当者へ共有します。保存期間や閲覧権限等は契約・初期導入時に決めます。</p></article><article><h3>店舗の判断が必要なときは連絡</h3><p>トラブルは店舗責任者または指定担当者へ連絡します。返金・キャンセル料・特殊対応の権限は導入時に決めます。</p></article></div></div></section>
<section class="section comparison-band"><div class="container"><div class="comparison-intro"><p class="eyebrow">受付・報告型との対応範囲の違い</p><h2>内容を受け取り、<br>予約の運用まで担う。</h2></div><div class="comparison"><div><h3>受付・報告型の一例</h3><p>電話を受ける<br>内容を確認する<br>店舗へ報告する</p></div><div><h3>スターズハブ</h3><p>複数窓口からの問い合わせ対応<br>空き確認・料金案内・予約調整・確定<br>予約表・台帳への反映<br>店舗・担当者への共有<br>変更・キャンセル対応</p></div></div><p class="fine-print">受付・報告型は契約範囲の一例です。他社サービスの対応範囲は事業者・プランによって異なります。スターズハブも、利用する環境と店舗のルールに合わせて対応方法を設計します。顧客履歴・注意事項・NG情報等は各対応で確認・更新します。</p></div></section>
<section class="section" id="setup"><div class="container split-section">{section_heading('04','導入の流れ','運用を確認してから、<br>スタート。')}<div>{onboarding(True)}</div></div></section><section class="section price-preview"><div class="container"><div><p class="eyebrow">予約受付の料金</p><h2>月額165,000円から。</h2><p>ベース50案件、スタンダード100案件、カスタム150案件〜。<br>対応量に合わせて選べる月額プランです。表示価格はすべて税込です。</p></div>{button('../pricing/','料金・案件の数え方を見る','button-outline')}</div></section><section class="section faq-section" id="faq"><div class="container split-section">{section_heading('05','ご相談の前に','よくある質問')}<div>{faq(questions+[FAQ_COUNT])}<a class="text-link faq-more" href="../pricing/">料金と初期費用を確認する{arrow()}</a></div></div></section>{cta(p)}'''

def pricing():
    p='../'
    extras=f'<div class="support-rates"><article><h3>媒体・求人コンテンツ制作</h3>{support_prices("content")}</article><article><h3>プロフィール文章制作</h3>{support_prices("profile")}</article><article><h3>掲示板対策</h3>{support_prices("board")}</article><article><h3>投稿モニタリング・個別対応</h3><dl class="rate-list"><div><dt>投稿モニタリング <small>月額</small></dt><dd>22,000円〜</dd></div><div><dt>問題投稿の個別対応 <small>1案件</small></dt><dd>33,000円〜</dd></div></dl><p class="fine-print">個別対応：内容確認、証拠保存、状況整理、今後の対応方針整理。法的な削除請求・発信者情報開示等の法律業務を行うサービスではありません。</p></article></div>'
    q=[FAQ_COUNT,FAQ_MULTI,('初期導入費には何が含まれますか？','<p>予約ルール、対応方法、連絡先、顧客情報の扱いを確認し、店舗に合わせた受付フローを設計します。初期導入費は通常33,000円、導入キャンペーン11,000円です。表示価格はすべて税込です。</p>'),('カスタムプランはどのように決まりますか？','<p>月額440,000円〜、150案件〜のプランです。受付量と運用内容を確認し、個別に設計・見積します。</p>')]
    return subhero(p,'料金・プラン','任せる受付量に、<br>合わせた料金。','予約成立の件数を基準に、月額プランを選べます。電話やLINEの連絡回数では数えません。表示価格はすべて税込です。')+f'''<section class="section pricing-detail"><div class="container"><div class="pricing-intro">{section_heading('01','予約受付・カスタマーサポート','一連の対応を、すべてのプランに。')}<p>予約受付・カスタマーサポート<br>顧客情報・対応履歴・注意事項の確認と記録<br>店舗・担当者への共有</p></div>{plan_table()}{price_notes()}<div class="price-consult">{actions(p)}</div></div></section>
<section class="section count-band" id="count"><div class="container"><p class="eyebrow">02　案件の数え方</p><h2 class="count-headline">予約成立<strong>1</strong>件 <span aria-hidden="true">＝</span> <strong>1</strong>案件</h2><p>原則として、成立した予約ごとに数えます。連絡回数で案件数が増える方式ではありません。</p><dl class="count-examples"><div><dt>同じお客様が2件予約</dt><dd><strong>2</strong>案件</dd><dd class="count-note">お客様が同じでも、成立した予約ごとに数えます。</dd></div><div><dt>予約に至らない問い合わせ</dt><dd><strong>0</strong>案件</dd><dd class="count-note">問い合わせのみで予約が成立しなかった場合は数えません。</dd></div><div><dt>同一予約の変更・キャンセル</dt><dd class="count-text">追加カウントなし</dd><dd class="count-note">後日の変更・キャンセルも、元の1案件のままです。</dd></div></dl></div></section>
<section class="section"><div class="container fees-layout">{section_heading('03','月額以外の費用','初期設計と、<br>超過分の料金。')}<div class="fees-detail"><article><p class="eyebrow">初期導入費</p><h3>受付フローを、店舗に合わせて設計。</h3><p>予約ルール・対応方法・連絡先・顧客情報の扱いを確認します。</p><div class="setup-price"><span>導入キャンペーン</span><strong>11,000<small>円</small></strong><p>通常33,000円</p></div></article><article><p class="eyebrow">超過料金</p><h3>標準案件数を超えた場合</h3><p class="overage-price">1案件 <strong>3,300</strong>円</p></article><p class="fine-print">表示価格はすべて税込です。</p></div></div></section>
<section class="section example-band"><div class="container split-section">{section_heading('04','料金例','月々の費用を、<br>具体的に。')}<div class="billing-examples"><article><p>ベースで月50案件の場合</p><h3>165,000<small>円 / 月</small></h3><p class="fine-print">月額165,000円。超過なし。</p></article><article><p>ベースで月55案件の場合</p><h3>181,500<small>円 / 月</small></h3><p class="fine-print">月額165,000円＋超過5案件×3,300円。</p></article><article><p>導入月にベースで50案件の場合</p><h3>176,000<small>円</small></h3><p class="fine-print">月額165,000円＋キャンペーン初期導入費11,000円。</p></article><p class="fine-print">表示価格はすべて税込です。上記は記載した月額・案件数・初期導入費で計算した例です。複数店舗は個別に設計・見積します。</p></div></div></section>
<section class="section support-pricing"><div class="container">{section_heading('05','別途ご相談いただける店舗運営支援','集客支援・評判／リスク対策。')}{extras}<p class="fine-print">表示価格はすべて税込です。集客支援・評判／リスク対策は、内容確認後、最短即日着手可能です。</p><a class="text-link" href="../reputation/">対応内容を確認する{arrow()}</a><div class="related-line"><p>Google口コミ獲得・運用の専門サービス</p><a href="https://kuchikomi-stars.com/" target="_blank" rel="noopener noreferrer">クチコミスターズ{arrow()}</a></div></div></section><section class="section faq-section" id="faq"><div class="container split-section">{section_heading('06','料金について','よくある質問')}{faq(q)}</div></section>{cta(p)}'''

def reputation():
    p='../'
    return subhero(p,'集客支援・評判／リスク対策','伝えること。<br>見守ること。','媒体・求人コンテンツ制作から、掲示板対策・投稿モニタリングまで。予約受付とは別にご相談いただける、店舗運営支援です。','subhero-sage')+'''<nav class="page-jump container" aria-label="ページ内メニュー"><a href="#growth">集客支援</a><a href="#risk">評判・リスク対策</a><a href="#monitoring">投稿モニタリング</a><a href="#industries">対応業種</a></nav>'''+f'''<section class="section" id="growth"><div class="container"><div class="support-detail-head">{section_heading('01','集客支援','店舗の情報を、<br>伝わる文章に。')}<p class="large-copy">掲載媒体や求人向けのコンテンツ、プロフィール文章を制作。媒体と目的に合わせて整えます。</p></div><div class="support-rates"><article><h3>媒体・求人コンテンツ制作</h3><p>媒体に掲載する情報や、求人向けコンテンツを制作します。</p>{support_prices('content')}</article><article><h3>プロフィール文章制作</h3><p>紹介する相手や、掲載先に合わせた文章を制作します。</p>{support_prices('profile')}</article></div><p class="fine-print">表示価格はすべて税込です。内容確認後、最短即日着手可能です。</p></div></section>
<section class="section risk-band" id="risk"><div class="container split-section">{section_heading('02','評判・リスク対策','店舗に関する投稿へ、<br>必要な対応を。')}<div><h3 class="large-copy">掲示板対策</h3><p>店舗に関する掲示板上の情報への対応と、状況把握を支援します。</p>{support_prices('board')}<p class="fine-print">表示価格はすべて税込です。内容確認後、最短即日着手可能です。</p></div></div></section>
<section class="section" id="monitoring"><div class="container"><div class="support-detail-head">{section_heading('03','投稿モニタリング','状況を把握し、<br>必要な情報を届ける。')}<p class="large-copy">掲示板・SNS等の投稿を確認。指定キーワードに関する投稿を検知し、LINE・メールで通知、履歴を記録します。</p></div><div class="monitor-layout"><article><p class="eyebrow">投稿モニタリング</p><h3 class="monitor-price">22,000<small>円〜 / 月</small></h3><div class="monitor-flow"><span>掲示板・SNSの投稿確認</span><span>店舗名・在籍者名・指定キーワードの検知</span><span>LINE・メールで通知、検知履歴を記録</span></div></article><article><p class="eyebrow">問題投稿の個別対応</p><h3 class="monitor-price">33,000<small>円〜 / 案件</small></h3><p>内容確認、証拠保存、状況整理、今後の対応方針整理を行います。</p><p class="fine-print">法的な削除請求・発信者情報開示等の法律業務を行うサービスではありません。</p></article></div><p class="fine-print">表示価格はすべて税込です。</p></div></section>
<section class="section industries" id="industries"><div class="container">{section_heading('04','対応業種','店舗の情報発信と、評判を支える。')}<ul class="industry-list"><li>アロマエステ</li><li>デリヘル</li><li>ホテヘル</li><li>ファッションヘルス</li><li>ソープ</li><li>その他予約型サービス</li><li>キャバクラ・ラウンジ</li><li>ガールズバー</li><li>ホストクラブ</li></ul><div class="related-line"><p>実店舗のGoogle口コミ獲得・運用は、専門サービスへ。</p><a href="https://kuchikomi-stars.com/" target="_blank" rel="noopener noreferrer">クチコミスターズ{arrow()}</a></div></div></section>{cta(p,'必要な運営支援を、<br>ご相談ください。')}'''

def contact():
    return subhero('../','お問い合わせ','任せたい業務から、<br>お聞かせください。','現在の受付方法や、お困りのことを分かる範囲でお聞かせください。対応内容と料金をご案内します。')+f'''<section class="section contact-section"><div class="container contact-layout"><div class="contact-guide"><p class="eyebrow">ご相談いただけること</p><h2>受付の運用から、<br>店舗運営支援まで。</h2><ul class="contact-services"><li>予約受付・カスタマーサポート</li><li>媒体・求人コンテンツ、プロフィール文章制作</li><li>掲示板対策・投稿モニタリング</li></ul><div class="contact-line"><h3>LINEでのご相談</h3><p>現在の運用や、ご希望の業務を<br>そのままお送りいただけます。</p>{line_link()}</div><p class="fine-print">予約受付に必要な設定や店舗ルールは、初期導入時に確認します。</p><p class="fine-print">お問い合わせに伴う情報の取り扱いは、<a href="../privacy/">プライバシーポリシー</a>をご確認ください。</p></div><div class="contact-mail"><p class="eyebrow">メールでお問い合わせ</p><h2>ご相談内容を送る</h2><p>下の項目を入力すると、メールの下書きを作成できます。メールアプリで内容を確認し、送信してください。</p><form class="email-draft" id="contact-form" action="mailto:{EMAIL}" method="get"><label for="store">店舗名・会社名 <span>任意</span></label><input id="store" name="store" autocomplete="organization" maxlength="100" placeholder="店舗名・会社名"><label for="name">ご担当者名 <span>任意</span></label><input id="name" name="name" autocomplete="name" maxlength="100" placeholder="お名前"><label for="service">ご希望のサービス</label><select id="service" name="service"><option>予約受付・カスタマーサポート</option><option>集客支援</option><option>評判・リスク対策</option><option>その他・サービス未定</option></select><label for="message">ご相談内容 <span>任意</span></label><textarea id="message" name="message" rows="5" maxlength="1000" placeholder="現在の受付方法、任せたい業務、困っていることなど"></textarea><button class="button button-primary" type="submit">メールアプリで下書きを開く{arrow()}</button><p class="fine-print form-note">この操作だけでは送信されません。</p></form><noscript><p>メールの下書き作成にはJavaScriptが必要です。下のメールアドレスから直接お問い合わせください。</p></noscript><div class="direct-email"><p>直接メールを送る場合はこちら</p><a href="mailto:{EMAIL}">{EMAIL}</a><button type="button" class="copy-email" data-copy-email="{EMAIL}">アドレスをコピー</button><span class="copy-status" role="status"></span></div></div></div></section>'''

def legal_page(path):
    # The article markup, text, date, and outbound links are intentionally exact.
    t=original(path)
    article=re.search(r'<article\b.*?</article>', t, re.S).group()
    label='プライバシーポリシー' if path.startswith('privacy') else '運営者情報'
    desc='お問い合わせ・予約受付等に伴う情報の取り扱いについて。' if path.startswith('privacy') else 'スターズハブの運営情報とお問い合わせ窓口です。'
    return subhero('../',label,label,desc)+f'<section class="section document-section">{article}</section>'

def not_found():
    return '''<section class="not-found"><div class="container"><p class="error-number" aria-hidden="true">404<span>✳</span></p><p class="eyebrow">404　ページが見つかりません</p><h1>お探しのページが<br>見つかりません。</h1><p>URLが変更されたか、ページが存在しない可能性があります。</p><div class="actions">'''+button('/','トップページへ')+button('/contact/','導入について相談する','button-outline')+'</div></div></section>'

def render(path, body):
    t=original(path)
    head=re.search(r'<head>(.*?)</head>',t,re.S).group(1).strip()
    head=head.replace('#1268E8','#102331')
    head=re.sub(r'(assets/site\.(?:css|js))(?=["\'])',rf'\1?v={VERSION}',head)
    head=head.replace('https://killerword.info/assets/ogp.png','https://killerword.info/assets/ogp.png?v='+VERSION)
    head=head.replace('スターズハブ STARS HUB。すべての予約受付を、ひとつに。予約受付・カスタマーサポート、集客支援、評判・リスク対策。','スターズハブ STARS HUB。すべての予約受付を、ひとつに。問い合わせ対応から予約確定、現場共有まで。')
    # UTF-8 must be identified before tag scripts, and within the first 1024 bytes.
    head=head.replace('<meta charset="utf-8">','')
    prefix='/' if path=='404.html' else ('../' if '/' in path else './')
    page_class='page-home' if path=='index.html' else 'page-'+path.split('/')[0].replace('.html','')
    result=f'<!doctype html>\n<html lang="ja"><head>\n<meta charset="utf-8">\n{head}\n</head>\n<body class="{page_class}">\n{header(prefix,path)}\n<main id="main">\n{body}\n</main>\n{footer(prefix,path)}\n</body></html>\n'
    (ROOT/path).write_text(result)

if __name__=='__main__':
    pages={'index.html':home(),'contact-center/index.html':contact_center(),'pricing/index.html':pricing(),'reputation/index.html':reputation(),'contact/index.html':contact(),'privacy/index.html':legal_page('privacy/index.html'),'legal/index.html':legal_page('legal/index.html'),'404.html':not_found()}
    for path,body in pages.items():
        render(path,body)
    print(f'Built {len(pages)} pages. Legal articles preserved from {BASE}.')
