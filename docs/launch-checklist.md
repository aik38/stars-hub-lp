# 公開チェックリスト

## 今回のGitHub Pages仮公開

- [ ] main・/(root)を公開元に設定
- [ ] https://aik38.github.io/stars-hub-lp/ の全ページを確認
- [ ] 全HTMLの `noindex, nofollow` を確認
- [ ] `robots.txt`: `User-agent: *` / `Disallow: /` を確認
- [ ] PC・スマホ、内部リンク、LINE・メール、FAQ・メニューを確認
- [ ] 保全対象repoのmain HEADが `ff3b3266c7a91c61b2211cf70f00226f75687a1e` のままであることを確認
- [ ] https://kuchikomi-stars.com/ の正常表示を確認

## 将来の本番公開（今回は実行しない）

- [ ] 運営主体・代表者・所在地表記とプライバシーポリシーの確認
- [ ] 未確定の契約条件が確定した際の案内範囲を確認
- [ ] `killerword.info` の現行設定・リダイレクトを保全し、切替手順を確認
- [ ] CNAMEを本番用として作成・設定（今回の仮公開には作成しない）
- [ ] Cloudflareの現行Redirect Rule等を確認・保全
- [ ] ウェブ用DNSの設定・切替を確認
- [ ] HTTPS証明書・強制HTTPS・HTTPからの転送を確認
- [ ] wwwの使用有無と転送先を確認
- [ ] 全ページのnoindex解除
- [ ] robots.txtの公開用設定への変更
- [ ] 各ページのcanonical設定
- [ ] 各ページのog:url設定
- [ ] OGPのタイトル・説明・共有画像を作成・確認
- [ ] 本番sitemapの作成・公開
- [ ] GA4の採用・設定・計測確認（必要な場合のみ）
- [ ] Search Consoleの登録・確認
- [ ] 本番ドメイン配下での内部リンク・404のルートリンクを確認
- [ ] LINE URLと遷移先の確認
- [ ] メールアドレス表示・mailtoの確認
- [ ] メールDNSの保全：MX・SPF・DKIM・DMARCを変更しない
- [ ] Google Workspace、既存メールの送受信を保全
- [ ] `kuchikomi-stars.com` / `review.kuchikomi-stars.com` / 既存repo / GA4・Search Consoleを保全

仮Pages配下のrobots.txtは、そのドメイン直下のrobots.txtの代替にはなりません。全ページのnoindexも維持します。
