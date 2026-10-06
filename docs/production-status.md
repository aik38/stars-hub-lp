# 本番状態（2026年10月7日）

本番URL： https://killerword.info/

## 公開・検証済み

- 実装のmain反映前：`1dd7d9ebd2c58147fb7a1791828e53c777ce9b0a`。
- 本番実装commit：`8780b1fcd612578e18421cef206403d9a8da72a4`。
- 作業ブランチ：`work/full-site-completion-20261007`。実装と最終Docsを保存。
- 保全ブランチ：`backup/pre-full-site-completion-20261007`。反映前SHAを保持し、変更・削除していない。
- [Pagesデプロイ run 37515172122](https://github.com/aik38/stars-hub-lp/actions/runs/37515172122)：success。
- [全ページ・本番検証 run 37515172589](https://github.com/aik38/stars-hub-lp/actions/runs/37515172589)：success。
- 本番9ページとCSS・JS・favicon・OGP・robots・sitemap、合計16ファイルは実装内容とSHA-256で一致。
- 本番9ページ×1440・1024・768・390・360px、45/45通り合格。
- 存在しないURLはHTTP 404、共通デザインの専用404本文とトップへのリンクを確認。
- ブラウザでトップ・導入事例・受付・料金・集客支援／リスク対策・問い合わせ・privacy・legal・404を表示確認。

## 公開ページ

| URL | HTTP |
| --- | --- |
| https://killerword.info/ | 200 |
| https://killerword.info/contact-center/ | 200 |
| https://killerword.info/cases/ | 200 |
| https://killerword.info/pricing/ | 200 |
| https://killerword.info/reputation/ | 200 |
| https://killerword.info/contact/ | 200 |
| https://killerword.info/privacy/ | 200 |
| https://killerword.info/legal/ | 200 |
| https://killerword.info/404.html | 200 |

## 完成内容

トップは指定の軽微修正に限定。全詳細ページをトップの配色・フォント・幅・ヘッダー・フッター・CTAへ統一。導入事例は提供された30件を6分類で掲載。予約受付、料金・案件定義、集客支援とリスク対策、相談窓口を整理した。privacy・legalの本文は変更前と完全一致。

GA4は `G-8S2N18S2YX` を全9ページで維持。CNAMEは `killerword.info`。公開ページはindex、404はnoindex。sitemapは8URL。LINE・メール宛先を維持し、問い合わせフォームは設けていない。

README、design-spec、production-status、verification、launch-checklistを実装と確認結果へ同期。旧レビュー冒頭にHISTORICALを追記。旧検証HTML・JSONは日付付き履歴として保持し、現行結果は `responsive-results.json` へ保存。AGENTS.mdに参照順位と維持ルールを記録。

実装検証完了後の更新はDocsと検証workflowの実行条件のみで、公開HTML・CSS・JS・画像は変更していない。Docsだけの変更ではブラウザ検証を再実行せず、Pagesの公開結果を確認する。

Cloudflare・DNS・Google Workspace・メール・Search Consoleの設定は変更していない。
