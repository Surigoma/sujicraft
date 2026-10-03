# エンジニアリングの行動ルール

設計・実装・レビュー・Sujicraft自身の保守では、対象に対応するスキルを使用する。複数の対象を含む作業では必要なスキルを併用する。

[共通の意思決定原則](shared/principles.md)を常に確認する。複数のルールや選択肢が競合する場合は、そこで定めた優先順位と「Prefer the smallest justified change」に従う。行数・ファイル数や一般的なベストプラクティスだけで判断しない。

各SKILLは、上位原則を作業ごとに適用する具体的な手順と必須条件を定める。上位原則と具体的ルールの役割を混同せず、対象に関係する指示を併せて適用する。

作業ごとのルールは次のファイルにある。

- [設計](skills/engineering-design/SKILL.md)
- [コーディング](skills/engineering-code/SKILL.md)
- [コード・設計レビュー](skills/engineering-review/SKILL.md)
- [UIデザインレビュー](skills/ui-design-review/SKILL.md)：UIデザインは独立したスキルで確認する。
- [ドキュメントレビュー](skills/document-review/SKILL.md)：文書のレビュー・整理・校正に使用する。
- [プラグイン保守](skills/plugin-maintenance/SKILL.md)：Sujicraft自身のSKILL、設定、配布、版管理に使用する。
