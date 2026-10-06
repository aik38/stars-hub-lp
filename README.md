# STARS HUB

店舗の予約受付・カスタマーサポートを運用するスターズハブの公式サイト。

- 本番：https://killerword.info/
- GitHub：https://github.com/aik38/stars-hub-lp
- GitHub Pages：`main` / リポジトリ直下から公開。CNAMEは`killerword.info`。

## ページ

| URL | 目的 |
| --- | --- |
| `/` | 受付業務を任せる価値、対応業務、利用者の声、料金概要、対応業種、導入相談 |
| `/contact-center/` | 受付業務、顧客情報、変更対応、現場共有、既存環境、運用設計 |
| `/pricing/` | 3プラン、案件定義、初期導入費、超過料金、料金例、追加サービス |
| `/reputation/` | 集客支援、掲示板対策、投稿モニタリングと各料金 |
| `/contact/` | メール下書き作成、直接メール、LINE相談 |
| `/privacy/` | 個人情報・GA4等の取り扱い |
| `/legal/` | 運営者情報 |
| `/404.html` | 不明なURLからの復帰 |

## 実装と再生成

静的HTML、共通CSS、必要最小限のJavaScript、独自SVG。サイト表示にフレームワークやビルドサーバーは不要。外部フォントを読み込まない。

`tools/build_site.py`で共通ヘッダー・フッターと各ページを生成する。

```bash
python3 tools/build_site.py
python3 tools/check_site.py
node --check assets/site.js
```

生成元は承認済みの保全commit `5202d303876cfca3b6205ef61a1e07a3648e6947`。SEOのtitle・description・canonical等、GA4ブロックを引き継ぎ、privacy/legalの記事本文はHTMLも含めて完全に維持する。商品情報の変更時は、この保全元との整合も確認する。

`python3 -m http.server 8000`でリポジトリ直下を配信して確認できる。

## 検証

- 静的確認：`tools/check_site.py`。料金、案件定義、補助サービス、法務、内部リンク、GA4、canonical等。
- ブラウザ確認：`tools/browser_check.cjs`。Playwrightを別ディレクトリへインストールし、`PW_MODULE`にパスを設定して実行する。サイト自体にnpm依存はない。
- 対象：8ページ × 1440 / 1024 / 768 / 390 / 360 px、JavaScriptなし8ページ、FAQ、メニュー、固定CTA、遷移、404、メールアドレスコピー。
- 表示確認用ページ：`docs/redesign-check.html`（noindex）。検証用のiframe内ではGA4を読み込まない。元HTMLのタグは維持する。
- GitHub Actions：作業branchだけで検証を実行し、合格したスクリーンショット・結果・OGPを同じbranchへ保存する。

お問い合わせフォームは入力内容から`mailto:`の下書きを開く。自動送信・サーバー保存を行わず、ユーザーがメールアプリで送信する。JavaScriptなしの場合も直接メール・LINEを利用できる。

## 計測・公開設定

全8ページに既存GA4 `G-8S2N18S2YX` を維持。入力された個人情報を独自イベントでGA4へ送らない。robotsは検索を許可し、sitemap・本番canonical・OGPを設定済み。

2026年10月6日の全面再設計では、Cloudflare・DNS・メール・Google Workspace・Search Console・GA4管理設定を変更しない。保全branch `backup/current-lp-memo-20261006` を維持する。

`docs/`の過去の設計・仮公開記録は当時の履歴。現在の実装は本READMEと新しい検証結果を確認する。
