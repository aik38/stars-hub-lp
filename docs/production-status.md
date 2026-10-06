# 本番状態（2026年10月7日）

本番URL： https://killerword.info/

## 作業開始時の確認

- main：`1dd7d9ebd2c58147fb7a1791828e53c777ce9b0a`。
- 保全ブランチ：`backup/pre-full-site-completion-20261007`。上記SHAと一致。変更・削除しない。
- Pages：mainの `pages build and deployment`、run `37506543240`、success。
- 本番トップ：HTTPS 200、承認済みFV・文字ロゴ・ブルーの表示をブラウザで確認。
- GA4：全既存ページに `G-8S2N18S2YX`。CNAMEは `killerword.info`。

## 今回の実装

作業ブランチ：`work/full-site-completion-20261007`。

トップの指定された軽微修正、全詳細ページのデザイン統一、6分類30件の `/cases/` 新設、料金・受付・集客支援／リスク対策・相談窓口の整理、法務本文の維持、SEO・sitemap・OGP・favicon・README・Docsの同期を実装。

この作業ブランチの段階ではmainへ未反映。本番反映後に、公開commit・Pages結果・本番照合結果をこのファイルへ追記する。

Cloudflare・DNS・Google Workspace・メール・Search Consoleの設定は変更していない。
