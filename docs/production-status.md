# 本番公開準備状況（2026-10-05）

## 実施済み
- 開始時main: 811ff2f4b68f91fb55cf522ca6c060e291500649。
- backup/pre-killerword-production-20261005 を上記SHAから作成。
- mainで運営者情報を指定内容に修正。代表者欄と氏名を削除。
- mainのデプロイ成功、仮公開と既存クチコミスターズLPを表示確認。

## このブランチの変更
- killerword.infoを基準に8ページのcanonicalとog:urlを設定。
- 公開ページのnoindexを解除、robots.txtにAllowと本番sitemapを設定。
- sitemap.xmlは指定7URLのみ。404を除外。
- CNAMEをkillerword.infoに設定。
- 404の絶対パスを本番ルートに修正。
- 本文・料金・デザイン・CSS・JavaScriptは変更しない。

## 未実施・公開前に必要
- このブランチはmainへ未統合。GitHub Pagesのカスタムドメインも未設定。
- CloudflareとGA4管理画面のオープンは自動承認レビューが拒否。非公開DNS・分析アカウントへの明示的なアクセス承認が必要との理由。
- DNS / Proxy / Redirect Rules / Page Rulesの監査とメールDNSの前後比較は未完了。設定変更は一切していない。
- この実行環境からの公開DNS照会はNetwork is unreachable。Web取得でもDNSレコードは取得できなかった。
- killerword.infoのHTTPS訪問はGitHub PagesのSite not found画面。旧サイトへの転送はこの訪問では観測しなかった。全HTTP/wwwパターンは未検証。
- GA4のスターズハブ専用プロパティ・Webストリーム・測定IDは未作成。タグも未実装。
- GA4導入時のみprivacyのCookie・アクセス解析段落を最小限修正する。他の段落は維持。
- Search Consoleのドメインプロパティ・所有権確認・sitemap送信は未実施。
- GA4/SCのログイン、アカウント選択、本人確認、CAPTCHA、規約同意はユーザー操作で行う。
- 本番URLの主要7ページ、HTTPS、HTTP/www統一、リンク、計測は公開後に確認する。
- 既存のMX/SPF/DKIM/DMARC/Google Workspaceとクチコミスターズ各設定は変更しない。

## GA4導入時のCookie・アクセス解析段落案
本ウェブサイトでは、利用状況の把握と改善のためにGoogle Analyticsを利用しています。Google AnalyticsはCookie等を使用し、閲覧したページや端末・ブラウザ等のウェブサイト利用状況に関する情報を収集します。リンク先の外部サービスにおける情報の取扱いは、各サービスの案内をご確認ください。

※測定IDが発行され、タグを実装した時点で反映する。現時点のprivacyは導入前の事実を維持している。
