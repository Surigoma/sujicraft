# Codexプラグインの配布検証

検証日：2026-10-03

## 作成した構成

- plugin.json：ポータブル形式のプラグイン設定
- .codex-plugin/plugin.json：Codex互換設定
- .claude-plugin/plugin.json：Claude Code・Grok Build互換設定。v0.2.0で追加
- .agents/plugins/marketplace.json：ローカル配布カタログ
- skills：6つのSKILL。Sujicraft自身の保守用SKILLを含む
- shared：既存の共通原則。各SKILLからの相対参照を維持
- scripts/package.py：標準ライブラリによる基本検証とZIP生成
- tests/test_package.py：ZIP展開・移設・参照欠損検知・CLI認識のチェック

外部サービスの接続、MCP、実行フックは追加していない。作者・公開URL・ライセンスは未指定のため、推測で設定していない。公開ディレクトリへの申請は行っていない。

## 実行して成功した確認

- JSON設定の読み込み、名前・バージョン・表示設定の一致
- 一覧用ロゴとコンポーザー用アイコンの設定、および配布物内の参照先
- ローカル配布カタログからプラグインルートへの対応
- 6つのSKILLの名前・説明の基本形式
- 全Markdown文書のUTF-8読み込み・300行上限・ローカルリンク先
- 配布ZIPの生成とCRC検査
- 一時ディレクトリへ展開したZIPの再検証
- 元のSKILLと共通原則がZIP内とバイト単位で一致すること
- 共通原則を欠損させた場合に、参照エラーとして検知すること
- 展開先を一時的なローカル配布元として指定し、Codex CLIがsujicraft@sujicraft-validation、バージョン0.1.0を利用可能として返すこと
- ローカル配布元からv0.1.0を再インストールし、キャッシュ内の版、6つのSKILL、plugin-maintenanceの内容がソースと一致すること

最初の設定なしの一覧取得ではこの配布元は表示されなかった。この環境のCLIでの検証には、コマンド単位のmarketplaces設定を使用した。通常の利用では、導入手順にある配布元登録が必要となる場合がある。

## 再実行

リポジトリのルートから実行する。

```powershell
python scripts/package.py
python tests/test_package.py
```

チェックは一時ディレクトリへ展開し、終了時にその一時領域を片付ける。Codex CLIが利用できない環境ではCLI認識のみSKIPと表示する。ユーザーの配布元登録、プラグインのインストール、有効化は行わない。

## 未検証

- アプリのプラグイン一覧での表示・インストール操作
- 新しいチャットでの自動選択・明示呼び出し・判断結果
- UIレビュー用の実アプリの表示・操作
- 他のCodexバージョンや他OSでの互換性
- 公式のJSON Schema・汎用YAMLバリデーターによる検証
- skill-creatorのquick_validate.pyによる検証（実行環境にPyYAMLがないため未実行）

配布ファイルの構成・移設・CLIでの認識・インストール済みキャッシュは確認済みだが、新しいチャットでのSKILL選択と実際の判断結果は未検証。

## 次の確認

アプリを再起動し、新しいチャットでplugin-maintenanceの自動選択・明示呼び出しと共通原則の読み込みを確認する。

仕様は [OpenAI公式のプラグイン配布資料](https://developers.openai.com/plugins/build/plugins)を参照した。CLIの一時設定は [公式設定リファレンス](https://learn.chatgpt.com/docs/config-file/config-reference)に従う。
