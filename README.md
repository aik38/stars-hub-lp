# STARS HUB LP

スターズハブの予約受付・カスタマーサポートを案内する静的サイトです。

- GitHub: https://github.com/aik38/stars-hub-lp
- GitHub Pages仮URL: https://aik38.github.io/stars-hub-lp/
- 将来の本番予定ドメイン: `killerword.info`（今回は接続しません）

## ページ構成

| パス | 内容 |
| --- | --- |
| `/` | トップページ |
| `/contact-center/` | 予約受付・カスタマーサポート |
| `/reputation/` | 集客・評判対策・ネット監視 |
| `/pricing/` | 料金 |
| `/contact/` | LINE・メールでのお問い合わせ |
| `/privacy/` | プライバシーポリシー |
| `/legal/` | 運営者情報 |
| `/404.html` | ページが見つからない場合の案内 |

仮URLでは、上記パスの先頭に `/stars-hub-lp` が付きます。

## 使用技術

HTML、CSS、必要最小限のJavaScript、独自インラインSVG。フレームワーク・外部フォント・外部JavaScript・解析タグ・Cookieを使用しません。FAQはHTMLの`details`を使用し、JavaScriptが無効でも主要内容・ナビゲーション・FAQを利用できます。

## Pages公開方法

GitHubのSettings → Pages → Build and deploymentで、Sourceを **Deploy from a branch**、Branchを **main**、フォルダを **/(root)** に設定します。`.nojekyll` により、HTML等をそのまま配信します。変更はmainへのcommitで再公開されます。

ローカル確認: このリポジトリの親フォルダで `python -m http.server 8000` を実行し、`http://localhost:8000/stars-hub-lp/` を開きます。

## 仮公開と本番切替

全HTMLに`noindex, nofollow`、`robots.txt`に`Disallow: /`を設定しています。仮公開中は検索掲載を意図しません。robots.txtはドメイン直下のファイルを参照する仕様のため、プロジェクトPages配下では各ページのnoindexも必須です。

今回はCNAME、独自ドメイン向けcanonical・og:url、sitemap、GA4、Search Consoleを設定していません。既存のクチコミスターズのリポジトリ・本番サイト・メール・DNSも変更対象外です。

本番切替前に、[公開チェックリスト](docs/launch-checklist.md)に沿ってドメイン・DNS・HTTPS・検索設定・OGP等を確認します。独自ドメインへの切替時には404ページのルートリンクも更新します。

## 設計と検証

- [デザイン仕様](docs/design-spec.md)
- [公開チェックリスト](docs/launch-checklist.md)
- [検証記録](docs/verification.md)
- [画面幅・公開HTTP応答の確認用ページ](docs/responsive-check.html)

料金・案件定義・サービス内容・CTAは2026年10月5日の制作指示に準拠します。最低契約期間、解約・返金条件、支払期限、SLA等の未確定条件は掲載していません。
