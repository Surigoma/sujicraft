# Grok Buildへの導入

Sujicraft v0.2.1はGrok BuildのClaude Code互換プラグイン読み込みを利用する。`.claude-plugin/plugin.json`、6つのSKILL、共通原則を共有する。

## ローカル読み込み

配布ZIPを展開したsujicraftフォルダーまたはこのリポジトリの絶対パスを指定し、作業対象のプロジェクトで起動する。

```powershell
grok plugin validate "C:\path\to\sujicraft"
grok plugin install "C:\path\to\sujicraft"
```

インストール時の確認画面で信頼対象を確認する。作業対象のプロジェクトで `grok` を起動し、`/plugins` と `/skills` でSujicraftと6つのSKILLを確認する。表示された名前で対象SKILLを呼び出す。

フォルダー全体を保持し、skillsだけを切り出さない。Grok BuildはAGENTS.mdも読むため、このリポジトリの保守用AGENTS.mdを別プロジェクトへ無条件でコピーしない。

## マーケットプレイスから導入

リポジトリを配布元として登録する場合は `.claude-plugin/marketplace.json` の一覧が使われる。Sujicraftを1件掲載している。

すでに登録した配布元が0 pluginsになっている場合は、修正版がGitHubへ反映された後に `grok plugin marketplace update https://github.com/Surigoma/sujicraft` を実行し、Grok Buildを再起動する。`/plugins` のMarketplaceからSujicraftを選んでインストールする。

登録と更新のコマンドは利用中の `grok plugin marketplace --help` で確認する。

## 更新と検証

ソースまたは展開済みフォルダーを更新し、CLIの `grok plugin update --help` で更新方法を確認して、新しいセッションで読み直す。実施状況は [対応環境の検証記録](../../validation/compatibility.md) を参照する。

ZIPは [Codex導入手順](../codex/README.md) の生成コマンドで作る。既存名の `-codex.zip` にGrok Build用の互換設定も同梱する。

[Grok Build公式仕様](https://docs.x.ai/build/features/skills-plugins-marketplaces) はClaude Code形式への互換性を明記している。公式資料には `--plugin-dir` もあるが、この環境の1.0.46にはないため、CLI helpで確認したローカルインストールを採用する。
