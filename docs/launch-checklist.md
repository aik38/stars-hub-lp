# 本番更新チェックリスト

2026年10月7日の更新・本番検証は完了。次の更新では各項目を再確認する。

初回仮公開用ではなく、`https://killerword.info/` の更新に使用する。

- [x] 開始時main・作業ツリー・Pages公開commit・本番表示を確認する。
- [x] 保全ブランチ `backup/pre-full-site-completion-20261007` が `1dd7d9ebd2c58147fb7a1791828e53c777ce9b0a` を指すことを確認し、変更しない。
- [x] 作業ブランチで実装し、トップ基準と `docs/design-spec.md` に整合させる。
- [x] 法務本文、提供事例、料金・案件定義に不用意な変更がないことを確認する。
- [x] 9ページ×5画面幅、ナビ、FAQ、CTA、表、長文、フッターを検証する。
- [x] 内部リンク・アンカー・title・description・canonical・OGP・Twitter・404を確認する。
- [x] GA4測定ID・CNAME・robots・8URLのsitemapを確認する。
- [x] 実際の完成内容でREADME・design-spec・verificationを更新し、過去資料を区別する。
- [x] 最終差分を確認し、main HEADを再取得して安全に反映する。
- [x] GitHub Pagesの本番commitのデプロイ成功を確認する。
- [x] 本番全ページ・アセットがcommit内容と一致することを確認する。
- [x] 本番の5画面幅・操作・404を確認し、production-status・verificationへ結果を記録する。

DNS・Cloudflare・メール・Google Workspace・Search Console設定の変更は含まない。
