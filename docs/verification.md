# 実装・本番検証記録

検証対象：2026年10月7日のサイト全体完成版。

## 開始時

main `1dd7d9ebd2c58147fb7a1791828e53c777ce9b0a` と保全ブランチの一致、Pages run `37506543240` のsuccess、本番トップの表示を確認。

## 静的確認

- 9ページの内部リンク・アセット226参照に欠落なし。内部アンカーも解決。
- 提供された事例30件を6分類で掲載。業態・店舗数・数値を維持。
- privacy・legalのmain内HTMLは変更前と完全一致。
- トップのFV・図・業務フロー・料金・FAQ・CTA構造とtop.jsを維持。top.cssは先頭コメントだけ更新。
- GA4 `G-8S2N18S2YX` とCNAME・robotsを維持。sitemapは `/cases/` を含む8URL。
- 全ページのcanonical・OGP・Twitter・descriptionを整合。404のみnoindex。
- LINEとmailto宛先を維持。問い合わせフォームなし。

## ブラウザ検証

`scripts/verify-site.mjs` と `Verify STARS HUB site` が9ページ×1440・1024・768・390・360pxの45通りを検証する。

横スクロール、要素のはみ出し、見出し、metadata、GA4コード、共通CSS、タップ領域、事例数、JavaScript例外、モバイルナビ開閉・Escape・リンク遷移、FAQ開閉、JavaScriptなしの回答と相談導線を確認する。テスト中のGA4送信は遮断する。

作業ブランチ `cc7265f1c3075058727f816db61f4512ac6bc23f` の検証run [37514675437](https://github.com/aik38/stars-hub-lp/actions/runs/37514675437) はsuccess。45/45通り合格、失敗0。予約受付1440pxと料金390pxの画面も確認し、共通デザイン・表・長文の折り返し・余白を確認した。本番照合結果は公開後に追記する。実機固有のOS・ブラウザ差とGA4管理画面上の受信結果は対象外。

## 過去の資料

`responsive-check-20261005.html`、`responsive-results-20261005.json`、日付付き画像と旧レビューは履歴。現行の検証結果ではない。
