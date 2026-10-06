# 実装・本番検証記録

## 技術SEO最終最適化（2026年10月7日）

唯一の実行正本：`STARS_HUB_技術SEO最終最適化_厳格版_Work指示_2026-10-07.txt`。

### 開始時と保全

main `cc9946e0af57222f80edeb082c5f1ea84ae59dfd` を再取得し、[Pages run 37520918673](https://github.com/aik38/stars-hub-lp/actions/runs/37520918673) のsuccessと本番8公開ページ・404.html・対象アセットのHTTP 200、存在しないURLのHTTP 404を確認。このmainから `backup/pre-technical-seo-20261007` と `work/technical-seo-20261007` を作成。main反映前に全backup branchとmainのSHAを再取得し、開始時と一致することを確認した。

### 実装と静的監査

- HTML変更は8公開ページのhead内のJSON-LD追加のみ。トップにWebSite・Organization、詳細7ページに表示中の「トップ / 各ページ名」と一致するBreadcrumbList。所在地は現在のlegal本文と完全一致することを機械検証。404にJSON-LDは追加しない。
- 各JSONをパースし、種類・項目・値を検証。価格・Review・AggregateRating・Product・Offer・Service・SearchAction・FAQPageの追加なし。
- canonical・og:urlは全9ページが自身の絶対URLと一致。公開8ページはindex可能、404は既存の `noindex, follow`。robotsはAllowとsitemap参照を維持。XMLパースしたsitemapは公開8URLのみ、404・changefreq・priority・lastmodなし。
- OGP/Twitter画像・favicon参照、lang、1H1、header/main/nav/footer、button/a、alt、aria、skip linkを確認。9ページの227内部リンク／アンカー／アセット参照は欠落なし。LINE・クチコミスターズ・mailtoの参照も変更なし。
- GA4 `G-8S2N18S2YX` は全9ページに各1読み込み・config。既存JSのdeferとGoogle Fonts preconnectを維持。404資源・重複した表示用読み込みなし。
- `python scripts/verify-static.py`、`python scripts/verify-seo.py --baseline-ref cc9946e0af57222f80edeb082c5f1ea84ae59dfd`、`node --check scripts/verify-site.mjs`、`git diff --check` は合格。

### 表示・文章・料金の差分

開始時mainと比較し、9ページの追加JSON-LDを除くHTML全体・bodyが完全一致。CSS2ファイル・top.js・favicon・OGP、合計5アセットとrobots・sitemap・CNAMEもバイト一致。title・description・OG/Twitterの文章、全本文・見出し・CTA・料金・投稿モニタリングの説明／料金表記を保持。表示用のタグ構造・スタイル・画像を変更していないため、デザイン・配色・フォント・余白・レイアウトも維持した。

検証workflowで変更前mainを別ポート配信し、同じviewportでブラウザの `body.innerText` を比較。作業ブランチ45/45通りで可視テキスト差分0・SHA-256一致。[作業ブランチ run 37524801688](https://github.com/aik38/stars-hub-lp/actions/runs/37524801688) はsuccess。FAQの開閉・モバイルナビの開閉／Escape／料金への遷移、料金・投稿モニタリングの既存検証も合格。

### main・本番確認

実装commit：`0e75ceee6426f7e9374416cdb683115eb6ab8f0b`。[Pages run 37525235235](https://github.com/aik38/stars-hub-lp/actions/runs/37525235235) はbuild・deployともsuccess。[main・本番 run 37525235904](https://github.com/aik38/stars-hub-lp/actions/runs/37525235904) はsuccess。ローカル45通り・本番45通り、全90通りで可視テキスト差分0・JSON-LD検証合格。

本番9ページと対象アセット計16ファイルは実装内容とSHA-256一致。公開8ページ・404.html・OGP/Twitter画像・favicon・CSS・JS・robots・sitemapはHTTP 200。存在しない `/missing-page-verification-20261007/` はHTTP 404で、専用404本文と「トップページへ戻る」を確認。404のnoindex、公開ページのindex可能状態、canonical・robots・XML sitemap・GA4維持を確認した。

| 画面幅 | 本番合格 | 可視テキスト差分 | 横スクロール・はみ出し |
| --- | --- | --- | --- |
| 1440px | 9 / 9 | 0 | なし |
| 1024px | 9 / 9 | 0 | なし |
| 768px | 9 / 9 | 0 | なし |
| 390px | 9 / 9 | 0 | なし |
| 360px | 9 / 9 | 0 | なし |

全幅で1H1・landmark・canonical/OGP/Twitter・GA4・料金・投稿モニタリング、CTAのタップ領域、FAQ・モバイルナビ、JavaScript例外なしを検証。JSなしのFAQ回答・モバイル相談導線も合格。画面のピクセル比較は実施せず、body・表示用アセットの完全一致と実ブラウザの全幅検証により表示維持を確認した。

検証画像の料金390px・集客支援／リスク対策360px、本番ブラウザでトップの料金表示と投稿モニタリングの「料金は内容に応じてご案内します。」を確認。ブラウザ検証時はGA4送信を遮断する。Analytics・Search Console管理画面と外部インフラ設定は操作しない。GA4の受信結果・検索順位・インデックス登録状況は今回の対象外。

現行の全幅結果は [responsive-results.json](responsive-results.json)。最終Docs同期は公開HTML・CSS・JS・画像を変更しない。README・AGENTS・日付付きHISTORICAL資料と事業仕様は維持する。

## 前回の料金差分時の記録（履歴）

以下は料金差分時の履歴。料金の事業仕様は維持し、今回の技術SEOでは変更していない。

## 開始時と保全

main `13077b51920a17c6c786666799ae982c7a53f556` を再取得し、Pages run `37515948768` のsuccessと本番3ページの旧料金状態を確認。ここから `backup/pre-pricing-refinement-20261007` と `work/pricing-refinement-20261007` を作成。既存 `backup/pre-full-site-completion-20261007` は `1dd7d9ebd2c58147fb7a1791828e53c777ce9b0a` のまま維持。main反映前に4ブランチのSHAを再確認した。

## 静的確認と差分

- 9ページ・内部リンク／アンカー／アセット227参照に欠落なし。
- トップと料金ページの補足・FAQは「規定件数を超える場合：1案件 1,650円（税込）」へ統一。料金ページのdescription・OG・Twitterも更新。
- 現行9ページの旧追加案件単価・旧見出し残存を検査。現行design-spec・READMEを新仕様へ同期し、HISTORICALの過去資料は変更していない。
- `/pricing/` は周辺サービス5項目の概要のみ。複数店舗・受付量の説明後、FAQ前に配置し、詳細へリンク。
- `/reputation/` の媒体制作4段階・プロフィール文章2メニュー・掲示板対策4段階を、件数／文字数と価格の組み合わせで検査。プロフィールの内包、初回100件1店舗1回まで、投稿モニタリングの個別案内、クチコミスターズの外部リンクを確認。
- 月額3段階・初期費用の元HTMLが一致。変更3ページのヘッダー・フッター・CTAも修正前と完全一致。
- 予約受付・事例・問い合わせ・privacy・legal・404・top.js・CNAMEは修正前と同一。デザインのトークン、GA4、robots、8URLのsitemapを維持。
- `python scripts/verify-static.py`、`node --check scripts/verify-site.mjs`、`git diff --check` は合格。

## ブラウザ・本番検証

実装commit：`f6acea1995405053ec8309ea1dcd71fe8fa330b9`。

[作業ブランチ run 37519775080](https://github.com/aik38/stars-hub-lp/actions/runs/37519775080) は45/45通り合格。[main・本番 run 37520130678](https://github.com/aik38/stars-hub-lp/actions/runs/37520130678) はsuccess。ローカル45通り、本番45通りが合格。公開9ページ・アセット計16ファイルは実装内容とSHA-256で一致。[Pages run 37520130996](https://github.com/aik38/stars-hub-lp/actions/runs/37520130996) はsuccess。

| 画面幅 | 本番の合格ページ数 | 横スクロール・はみ出し |
| --- | --- | --- |
| 1440px | 9 / 9 | なし |
| 1024px | 9 / 9 | なし |
| 768px | 9 / 9 | なし |
| 390px | 9 / 9 | なし |
| 360px | 9 / 9 | なし |

新たに、追加案件単価が14px・`#4B5158`で初期導入費22pxより小さいこと、料金概要の掲載位置と5項目、詳細料金の10行の正確な組み合わせとサービス内の配置を全5幅で確認した。

既存のFAQ開閉、モバイルナビ開閉・Escape・料金への遷移、CTAのタップ領域、見出し、canonical・OGP・Twitter・GA4コード、フォーム未設置、30事例、JavaScript例外、JSなしのFAQ・相談導線の確認も合格。テストのGA4送信は遮断する。

1440pxの料金・周辺サービス詳細、360pxの両ページの画像を確認。スマホの追加案件単価と「税込」、プロフィールの「キャッチコピー3本」がまとまって折り返されることを確認した。証跡画像はworkflow artifactに保存。

本番トップ・料金・周辺サービス詳細はHTTP 200、検証済みcommitの本文ソースと一致。ブラウザでも新料金・詳細リスト・料金FAQを確認し、トップの料金の強弱を実表示で確認。全9ページと対象アセットはHTTP 200。存在しないURLはHTTP 404、専用404本文とトップへのリンクを確認した。

この時点の全幅結果は当該workflow artifactを参照。この後のDocs同期は公開ファイルを変更しない。実機固有のOS・ブラウザ差、GA4管理画面の受信結果、外部サービスの設定は検証対象外。

## 前回のサイト全体完成時の記録（履歴）

以下は前回のサイト全体完成版の検証履歴。現行の料金仕様・検証結果は上記を参照。

### 開始時

main `1dd7d9ebd2c58147fb7a1791828e53c777ce9b0a` と保全ブランチの一致、Pages run `37506543240` のsuccess、本番トップの表示を確認。

### 静的確認

- 9ページの内部リンク・アセット226参照に欠落なし。内部アンカーも解決。
- 提供された事例30件を6分類で掲載。業態・店舗数・数値を維持。
- privacy・legalのmain内HTMLは変更前と完全一致。
- トップのFV・図・業務フロー・料金・FAQ・CTA構造とtop.jsを維持。top.cssは先頭コメントだけ更新。
- GA4 `G-8S2N18S2YX` とCNAME・robotsを維持。sitemapは `/cases/` を含む8URL。
- 全ページのcanonical・OGP・Twitter・descriptionを整合。404のみnoindex。
- LINEとmailto宛先を維持。問い合わせフォームなし。

### ブラウザ検証

`scripts/verify-site.mjs` と `Verify STARS HUB site` が9ページ×1440・1024・768・390・360pxの45通りを検証する。

横スクロール、要素のはみ出し、見出し、metadata、GA4コード、共通CSS、タップ領域、事例数、JavaScript例外、モバイルナビ開閉・Escape・リンク遷移、FAQ開閉、JavaScriptなしの回答と相談導線を確認する。テスト中のGA4送信は遮断する。

作業ブランチ `cc7265f1c3075058727f816db61f4512ac6bc23f` の検証run [37514675437](https://github.com/aik38/stars-hub-lp/actions/runs/37514675437) はsuccess。45/45通り合格、失敗0。予約受付1440pxと料金390pxの画面も確認し、共通デザイン・表・長文の折り返し・余白を確認した。本番検証は以下のとおり完了。実機固有のOS・ブラウザ差とGA4管理画面上の受信結果は対象外。

### 過去の資料

`responsive-check-20261005.html`、`responsive-results-20261005.json`、日付付き画像と旧レビューは履歴。現行の検証結果ではない。

### 本番確認結果

実装commit：`8780b1fcd612578e18421cef206403d9a8da72a4`。

[本番検証run 37515172589](https://github.com/aik38/stars-hub-lp/actions/runs/37515172589) はsuccess。ローカル配信45通り、本番45通りの両方が合格。公開後のページ・アセット16ファイルは、実装内容とSHA-256で完全一致。

| 画面幅 | 本番の合格ページ数 | 横スクロール・はみ出し |
| --- | --- | --- |
| 1440px | 9 / 9 | なし |
| 1024px | 9 / 9 | なし |
| 768px | 9 / 9 | なし |
| 390px | 9 / 9 | なし |
| 360px | 9 / 9 | なし |

モバイルナビの開閉・Escape・リンク遷移、FAQの開閉、CTAのタップ領域、料金表・長文・フッター、canonical・OGP・Twitter・GA4コード・フォーム未設置を確認。JavaScriptなしでもFAQ回答、モバイルの相談導線、共通フッターを利用できる。ブラウザ例外なし。

本番9ページ・全対象アセットのHTTP 200を確認。存在しない `missing-page-verification-20261007/` はHTTP 404で、専用404本文と「トップページへ戻る」を確認。本文ソースの内部リンク・アンカー・アセット226参照に欠落なし。

ブラウザでも本番のトップ・事例・受付・料金・集客支援／リスク対策・問い合わせ・privacy・legal・404を実表示し、見出しと内容を確認。予約受付1440px・料金390pxの画面と本番事例の視覚確認も実施。

この時点の全幅結果は当該workflow artifactを参照。実機固有のOS・ブラウザ差、GA4管理画面上の受信結果、外部サービス側の設定は検証対象外。テストのGA4送信は遮断し、タグと測定IDの維持を確認した。
