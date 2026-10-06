# STARS HUB

本番URL： https://killerword.info/

予約受付・カスタマーサポートの全体像から、任せられる業務、導入効果、料金、相談窓口までを案内する営業サイトです。集客支援とリスク対策も掲載しています。

現行の追加案件単価は **規定件数を超える場合：1案件 1,650円（税込）**。`/pricing/` に集客支援・リスク対策の料金概要、`/reputation/` に正本の詳細料金を掲載しています。金額と掲載方針は [design-spec](docs/design-spec.md) を参照してください。

## ページ構成

| URL | 役割 |
| --- | --- |
| `/` | サービス全体像の要約 |
| `/contact-center/` | 受付・管理・共有の業務範囲と運用 |
| `/cases/` | 6分類・30件の導入事例・お客様の声 |
| `/pricing/` | 予約受付の月額・初期費用・追加案件単価、案件定義、カウント例、周辺サービス料金概要、FAQ |
| `/reputation/#growth` | 媒体・求人コンテンツ制作とプロフィール文章の詳細料金、クチコミスターズ |
| `/reputation/#risk` | 掲示板対策の詳細料金、投稿モニタリング |
| `/contact/` | LINE・メールの相談窓口 |
| `/privacy/` | プライバシーポリシー |
| `/legal/` | 運営者情報 |
| `/404.html` | 存在しないURLからトップへ戻る案内 |

## 使用技術と公開

静的HTML・CSS・最小限のJavaScript。全ページは、承認済みトップの `assets/top.css` と `assets/top.js` を共有し、詳細ページの構造は `assets/details.css` で補います。Noto Sans JPはGoogle Fontsから読み込み、フォールバックも指定しています。

GitHub Pagesは `main` のルートを公開し、`.nojekyll` と `CNAME`（`killerword.info`）を使用しています。main更新後の `pages build and deployment` が本番更新を行います。GA4測定IDは `G-8S2N18S2YX`。canonical・OGP・Twitter情報とsitemapは本番URLに統一しています。404はnoindex、sitemapは8URLです。

LINE： https://lin.ee/X0mxy9O

メール： m-asakura@killerword.info

問い合わせフォームはありません。Cloudflare・DNS・Google Workspace・メール・Search Consoleの設定変更は、このサイト更新の対象外です。

## 設計と検証

- [現行デザイン正本](docs/design-spec.md)
- [本番状態](docs/production-status.md)
- [検証記録](docs/verification.md)
- [本番の全画面幅検証結果](docs/responsive-results.json)
- [本番更新チェックリスト](docs/launch-checklist.md)
- [実装時の参照順位](AGENTS.md)

2026年10月7日のサイト全体完成版指示に基づき、main `1dd7d9ebd2c58147fb7a1791828e53c777ce9b0a` のトップを基準として統一しています。保全ブランチ `backup/pre-full-site-completion-20261007` は変更しません。今回の料金差分は `STARS_HUB_料金表示・周辺サービス料金追加_Work指示_2026-10-07.txt` に基づき、修正前main `13077b51920a17c6c786666799ae982c7a53f556` のデザイン・配色・構成を維持しています。作業ブランチは `work/pricing-refinement-20261007`、今回の保全ブランチは `backup/pre-pricing-refinement-20261007`。日付付き旧レビュー・旧検証結果は履歴です。

ローカル表示：リポジトリ直下で `python -m http.server 8000` を実行し、`http://localhost:8000/` を開きます。

検証：`python scripts/verify-static.py`。ブラウザ検証は `scripts/verify-site.mjs` と `.github/workflows/verify-site.yml` で、9ページ×5画面幅を確認します。GA4へのテスト送信は遮断し、タグと測定IDの維持をソースで確認します。
