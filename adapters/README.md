# アダプター

実行環境ごとの配布用設定はここに置く。

Ponytailの移植性の考え方にならい、アダプターは必要最小限にし、行動ルールは `skills/` と `shared/` に置く。

配布形式：

- [Codexプラグイン](codex/README.md)：設定と導入手順を追加済み
- [Claude Codeプラグイン](claude-code/README.md)：共通SKILLのローカル読み込み
- [Grok Buildプラグイン](grok-build/README.md)：Claude Code互換形式のローカル読み込み
- OpenCodeプラグイン：未実装
- 必要に応じてGemini / Copilot / AGENTSのみの配布形式

マニフェストは各環境の公式仕様とCLIの実際の対応状況に基づいて追加する。検証範囲は [対応環境の検証記録](../validation/compatibility.md) を参照する。
