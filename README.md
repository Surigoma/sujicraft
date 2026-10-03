# Sujicraft

<img src="assets/branding/sujicraft-icon-joinery.png" alt="Sujicraft：コードの括弧と継ぎ手を組み合わせたアイコン" width="160" />

Sujicraft（スジクラフト）は、AIコーディングエージェント向けに、設計・実装・レビューの判断基準をまとめた個人用スキル集。「筋の通った」設計・実装・レビューを目指す。複数の実行環境で使える構成にし、会話と実例を通じて育てる。

Ponytailのように、行動ルールは `skills/`、共通原則は `shared/` に置く。実行環境ごとのアダプターは必要最小限にする。

## 現在のスキル

- [engineering-design](skills/engineering-design/SKILL.md)：設計と変更計画
- [engineering-code](skills/engineering-code/SKILL.md)：実装時の判断と進め方
- [engineering-review](skills/engineering-review/SKILL.md)：コード・設計のレビュー
- [ui-design-review](skills/ui-design-review/SKILL.md)：UIデザインのレビュー（情報構成・視線誘導・ユーザーフロー・見た目・アクセシビリティ）
- [document-review](skills/document-review/SKILL.md)：ドキュメントのレビュー・整理・校正
- [plugin-maintenance](skills/plugin-maintenance/SKILL.md)：Sujicraft自身のSKILL・設定・配布・版管理

## Codexへの導入

[導入手順](adapters/codex/README.md)に沿ってローカル配布元からインストールする。6つのSKILLと共通原則をまとめて配布する。

## 育て方

1. 安定した個人のエンジニアリング原則を `shared/principles.md` に置く。
2. 作業ごとの進め方を各 `skills/*/SKILL.md` に置く。
3. `AGENTS.md` は常時適用する指示として読み込めるよう、短く保つ。
4. 実行環境ごとのアダプターは、スキル本体を複製せず、参照または読み込みにとどめる。
5. 実際の仕事の具体例を通じて改善する。観察した成功・失敗に裏付けられたルールを優先する。

## 検証記録

[依頼例による机上評価](validation/scenarios.md)に、判断例と未確定事項を記録する。実環境での動作検証とは区別する。

[更新後の再検証](validation/revalidation.md)に、テスト確認とUI実画面検証の境界ケースを記録する。

## 現在の状態

v0の作成途中。共通原則と6つのスキルを整備しており、会話と実例を通じて判断基準を具体化する。Codex向けの配布設定とZIP生成を実装。検証範囲は [配布検証記録](validation/packaging.md) を参照する。
