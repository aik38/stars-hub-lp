# STARS HUB LP

スターズハブの予約受付・カスタマーサポートを案内する静的サイトです。

- 本番URL: https://killerword.info/
- GitHub: https://github.com/aik38/stars-hub-lp
- GA4測定ID: `G-8S2N18S2YX`

## ページ構成

| パス | 内容 |
| --- | --- |
| `/` | 業務範囲・電話代行との比較・料金・導入設計 |
| `/contact-center/` | 予約受付・カスタマーサポートの詳細 |
| `/reputation/` | 集客・評判対策とネットモニタリング、詳細料金 |
| `/pricing/` | 予約受付の料金・初期費用・超過料金・案件定義 |
| `/contact/` | LINE・メールでの相談 |
| `/privacy/` | プライバシーポリシー |
| `/legal/` | 運営者情報 |
| `/404.html` | ページが見つからない場合の案内 |

## 実装と公開

HTML、CSS、JavaScript、インラインSVGを使用しています。FAQと案件定義はHTMLの`details`で表示し、JavaScriptが無効でも閲覧できます。外部フォント・フレームワークは使用していません。アクセス解析にはスターズハブ専用のGA4タグを使用します。

GitHub Pagesはmainのルートから配信します。CNAME、canonical、sitemap、robotsは本番ドメインを基準とし、主要ページは検索公開状態です。

ローカル確認は、リポジトリ内で `python -m http.server 8000` を実行し、`http://localhost:8000/` を開きます。

## 検証記録

- [2026年10月6日の営業LP改善・検証](docs/sales-optimization-20261006.md)
- [画面幅・公開HTTP応答の確認用ページ](docs/responsive-check.html)
- [初回デザイン仕様](docs/design-spec.md)
- [初回制作時の検証記録](docs/verification.md)

料金金額と案件定義は確定仕様を維持しています。対応時間は店舗別に設定し、電話・LINE等の接続方法、予約サイトへの反映方法、導入日数、プラン内店舗数、緊急連絡の詳細は個別確認事項です。365日対応、固定SLA、最低契約期間、返金条件等の未確定条件は追加していません。
