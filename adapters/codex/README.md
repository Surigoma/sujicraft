# Codexプラグインの導入

## 配布物

ZIPを展開すると、sujicraftフォルダーに6つのSKILL、共通原則、プラグイン設定、ローカル配布カタログが入る。フォルダー全体を保持する。skillsだけを切り出すと共通原則への参照が切れる。

現在のバージョンは0.2.0。外部サービス、MCP、実行フックは含まない。自動選択を禁止する設定は追加していない。AGENTS.mdはこのリポジトリでの作業用指示であり、プラグインを入れた別プロジェクトへ常時適用されることは前提にしない。各SKILLは使用時に共通原則を参照する。

## ローカル導入

1. ZIPを利用する場合は展開する。
2. 展開したsujicraftフォルダーをCodexのプロジェクトとして開く。
3. プラグイン一覧で「Sujicraft」というローカル配布元を選び、「Sujicraft」をインストールする。
4. 必要に応じてアプリを再起動し、新しいチャットでスキルを確認する。

ローカル配布元が一覧に出ない場合、Codex CLIを利用できる環境では、展開したフォルダーから次を実行する。

```powershell
codex plugin marketplace add .
codex plugin list --marketplace sujicraft-local --available --json
```

この環境のCLIは次のインストールコマンドにも対応する。別バージョンでは、先にcodex plugin add --helpで対応を確認する。

```powershell
codex plugin add sujicraft@sujicraft-local
```

コマンドは利用者のCodex設定とキャッシュへ登録する。既存の個人用marketplace.jsonを上書きする必要はない。

## 呼び出しと確認

新しいチャットでスキル一覧から対象を選ぶか、スキル名を明示して依頼する。表示名はクライアントによりプラグイン名の接頭辞が付く場合がある。

- engineering-design：変更の設計
- engineering-code：実装
- engineering-review：コード・システム設計のレビュー
- ui-design-review：実画面でのUIデザインレビュー
- document-review：文章・構成・参照のレビューと校正
- plugin-maintenance：Sujicraft自身のSKILL・設定・配布・版管理

まず「engineering-designを使い、実装せず変更計画だけ示して」のように範囲を明示して試す。出力が共通原則を参照すること、承認条件を守ること、未検証の内容を明記することを確認する。具体例は [検証記録](../../validation/scenarios.md) を参照する。

## 更新・解除

ソースを編集しただけでは、インストール済みキャッシュに反映されたとは限らない。クライアントで更新または再インストールし、新しいチャットで確認する。

CLIで解除する場合は、対応するhelpを確認してから次を実行する。

```powershell
codex plugin remove sujicraft@sujicraft-local
codex plugin marketplace remove sujicraft-local
```

## ZIPの再生成

リポジトリのルートで実行する。Pythonの標準ライブラリのみを使用する。

```powershell
python scripts/package.py
python tests/test_package.py
```

dist/sujicraft-0.2.0-codex.zipを生成する。Claude Code・Grok Build用の互換マニフェストも含む。同名のZIPは再生成時に置き換える。スクリプトは設定の一致、アイコン参照、6つのSKILLの基本形式、300行上限、ローカル参照を確認する。JSON Schema全体や汎用YAMLの正式検証を代替するものではない。

## 仕様の参照元

構成とローカル配布方法は [OpenAI公式のプラグイン配布仕様](https://developers.openai.com/plugins/build/plugins) を確認した。ルートのplugin.jsonを基本とし、既存クライアント向けに.codex-plugin/plugin.jsonも同梱する。両者の表示設定は生成時に一致を確認する。

ローカル配布元の対応状況はクライアントにより異なる。実施済み・未実施の確認は [配布検証記録](../../validation/packaging.md) に記録する。
