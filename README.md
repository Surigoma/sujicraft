# Sujicraft

<img src="assets/branding/sujicraft-icon-joinery.png" alt="Sujicraft：コードの括弧と継ぎ手を組み合わせたアイコン" width="160" />

Sujicraft（スジクラフト）は、AIコーディングエージェント向けに、設計・実装・コミットメッセージ・レビューの判断基準をまとめた個人用スキル集。「筋の通った」設計・実装・レビューを目指す。複数の実行環境で使える構成にし、会話と実例を通じて育てる。

Ponytailのように、作業ごとの具体的なルールは `skills/`、競合時の優先順位を含む共通の意思決定原則は `shared/` に置く。実行環境ごとのアダプターは必要最小限にする。

## 現在のスキル

- [engineering-design](skills/engineering-design/SKILL.md)：設計と変更計画
- [engineering-code](skills/engineering-code/SKILL.md)：実装時の判断と進め方
- [commit-message](skills/commit-message/SKILL.md)：変更の前提・内容・結果を伝えるコミットメッセージの作成とレビュー
- [engineering-review](skills/engineering-review/SKILL.md)：コード・設計のレビュー
- [ui-design-review](skills/ui-design-review/SKILL.md)：UIの新規作成・変更時と明示的な依頼時のデザインレビュー（情報構成・視線誘導・ユーザーフロー・見た目・アクセシビリティ）
- [document-review](skills/document-review/SKILL.md)：ドキュメントのレビュー・整理・校正
- [plugin-maintenance](skills/plugin-maintenance/SKILL.md)：Sujicraft自身のSKILL・設定・配布・版管理

## Codexへの導入

[導入手順](adapters/codex/README.md)に沿ってローカル配布元からインストールする。7つのSKILLと[共通の意思決定原則](shared/principles.md)をまとめて配布する。

Claude CodeとGrok Buildでも同じ7つのSKILLを利用できる。[Claude Code導入手順](adapters/claude-code/README.md) と [Grok Build導入手順](adapters/grok-build/README.md) を参照する。検証範囲は [対応環境の検証記録](validation/compatibility.md) に記録する。

## 育て方

1. 複数の選択肢やルールが競合したときの上位の判断基準を `shared/principles.md` に置く。
2. 作業ごとの進め方を各 `skills/*/SKILL.md` に置く。
3. `AGENTS.md` は常時適用する指示として読み込めるよう、短く保つ。
4. 実行環境ごとのアダプターは、スキル本体を複製せず、参照または読み込みにとどめる。
5. 実際の仕事の具体例を通じて改善する。観察した成功・失敗に裏付けられたルールを優先する。

## 検証記録

[依頼例による机上評価](validation/scenarios.md)に、判断例と未確定事項を記録する。実環境での動作検証とは区別する。

[更新後の再検証](validation/revalidation.md)に、テスト確認とUI実画面検証の境界ケースを記録する。

## 現在の状態

v0の作成途中。共通の意思決定原則と7つのスキルを整備しており、会話と実例を通じて判断基準を具体化する。Codex向けの配布設定とZIP生成を実装。検証範囲は [配布検証記録](validation/packaging.md) を参照する。
