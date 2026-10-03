# Claude Code・Grok Build対応の検証

検証日：2026-10-03。対象版：0.2.0。

`.claude-plugin/plugin.json` を両環境で共有する。SKILLと共通原則は複製せず、ルートの `skills/` と `shared/` を利用する。

配布検証は3つのマニフェストの名前・版・説明、SKILL参照先、ZIP同梱、展開後の相対参照を確認する。互換マニフェストの版不一致を自動テストで検知する。

## 実行結果

- Claude Code 2.1.27：`claude plugin validate .` 成功。作者情報未指定の警告あり。作者情報を推測で追加していない。
- Grok Build 1.0.46：`grok plugin validate .` 成功。skillsディレクトリ1つを認識。
- Grok Buildのhelpでローカルパスからのインストール対応を確認。実際のユーザー環境へのインストールは未実施。
- 両CLIの検証は配布ZIPの一時展開先でも成功。Codexの認識、互換マニフェストの版不一致検知、共通原則・アイコンの欠損検知も成功。

## 未検証

- 両環境の対話セッションでのSKILL選択、共通原則の読み込み、判断結果
- 他バージョン・OSでの実行

利用方法は [Claude Code](../adapters/claude-code/README.md) と [Grok Build](../adapters/grok-build/README.md) を参照する。
