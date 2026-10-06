# 本番状態（2026年10月7日・料金差分）

本番URL： https://killerword.info/

## 公開・検証済み

- 今回の修正前main：`13077b51920a17c6c786666799ae982c7a53f556`。開始時の[Pages run 37515948768](https://github.com/aik38/stars-hub-lp/actions/runs/37515948768)はsuccess。
- 本番実装commit：`f6acea1995405053ec8309ea1dcd71fe8fa330b9`。この後のDocs同期は公開HTML・CSS・JS・画像を変更しない。
- 作業ブランチ：`work/pricing-refinement-20261007`。検証済み実装と最終Docsを保存。
- 今回の保全ブランチ：`backup/pre-pricing-refinement-20261007`。修正前mainを保持し、作成後は変更していない。
- 既存保全ブランチ：`backup/pre-full-site-completion-20261007`。`1dd7d9ebd2c58147fb7a1791828e53c777ce9b0a`を保持し、変更・削除していない。
- [実装のPages run 37520130996](https://github.com/aik38/stars-hub-lp/actions/runs/37520130996)：success。
- [作業ブランチ検証 run 37519775080](https://github.com/aik38/stars-hub-lp/actions/runs/37519775080)：success、45/45通り合格。
- [main・本番検証 run 37520130678](https://github.com/aik38/stars-hub-lp/actions/runs/37520130678)：success。ローカル45通り、本番45通りが合格。
- 本番9ページとCSS・JS・favicon・OGP・robots・sitemap、合計16ファイルが実装内容とSHA-256で一致。
- 本番9ページ×1440・1024・768・390・360px、45/45通り合格。横スクロール・はみ出しなし。
- 存在しないURLはHTTP 404で、専用404本文とトップへのリンクを確認。
- 本番トップ・料金・集客支援／リスク対策をブラウザで確認。料金FAQの新料金、トップの料金表と注記の強弱も確認。

## 今回の料金変更

規定件数を超える場合：**1案件 1,650円（税込）**。トップ・料金ページの補足とFAQ、料金ページのdescription・OG・Twitterを統一した。注記は14px・`#4B5158`で、初期導入費より低い視覚階層。金額と税込の語は途中で分割しない。

`/pricing/` に集客支援・リスク対策の料金概要と `/reputation/` への詳細リンクを追加。`/reputation/` に媒体制作4段階、プロフィール文章2メニュー、掲示板対策4段階と初回注記、投稿モニタリングの個別案内を追加。各金額は [design-spec](design-spec.md) に記録。クチコミスターズの料金は公式サイトへ案内する。

現行ページ・SEO情報に旧追加案件単価と旧見出しは残っていない。日付付きレビュー・旧検証資料は履歴として保持した。

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

## 維持・同期

完成済みのデザイン・配色・フォント・1200px幅・余白・ヘッダー・フッター・CTAを維持。予約受付の月額、初期費用、案件定義、30事例、法務・運営情報、top.jsは変更していない。

GA4は `G-8S2N18S2YX`、CNAMEは `killerword.info`。公開ページはindex、404はnoindex。sitemapは8URL。LINE・メール宛先を維持し、問い合わせフォームなし。

README、design-spec、production-status、verification、現行responsive-results.jsonを料金仕様と実際の結果へ同期。AGENTS.mdの参照順位と過去資料は維持。Docsのみの最終commitではブラウザ検証を再実行せず、Pagesの公開成功を確認する。

Cloudflare・DNS・Google Workspace・メール・Search Consoleの設定は変更していない。
