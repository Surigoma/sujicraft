# Claude Codeへの導入

Sujicraft v0.2.0は `.claude-plugin/plugin.json` とルートの `skills/` を使う。6つのSKILLと `shared/` はCodex・Grok Buildと共有する。

## ローカル読み込み

配布ZIPを展開したsujicraftフォルダーまたはこのリポジトリの絶対パスを指定し、作業対象のプロジェクトで起動する。

```powershell
claude --plugin-dir "C:\path\to\sujicraft"
```

セッションで `/sujicraft:engineering-design` などを呼び出す。6つのSKILLが表示され、共通原則が読めることを確認する。継続して使う場合も起動時に指定する。

skillsだけをコピーすると相対参照が切れるため、フォルダー全体を保持する。SujicraftのAGENTS.mdはこのリポジトリの保守用であり、別プロジェクトへの常時適用は前提にしない。

## 更新と検証

ソースまたは展開済みフォルダーを更新し、新しいセッションで読み直す。

```powershell
claude plugin validate "C:\path\to\sujicraft"
```

これはマニフェスト検証であり、モデルの選択・判断結果の検証とは区別する。実施状況は [対応環境の検証記録](../../validation/compatibility.md) を参照する。

ZIPは [Codex導入手順](../codex/README.md) の生成コマンドで作る。既存名の `-codex.zip` にClaude Code・Grok Buildの設定も同梱する。

[公式マニフェスト仕様](https://code.claude.com/docs/en/plugins-reference) と [公式プラグイン利用方法](https://code.claude.com/docs/en/plugins) に基づく。
