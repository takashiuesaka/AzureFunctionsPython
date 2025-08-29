## 目的

このドキュメントは、Azure Functions を Python（3.11）で実装する際のベストプラクティスと実装上の注意点を簡潔にまとめた指示書です。

前提

- 本リポジトリでは Azure Functions の official blueprint（テンプレート）をベースにプロジェクトを構成する前提とします。
- 各 HTTP / Queue 等のエンドポイント（Function 実装）はすべて `endpoints/` フォルダ配下に作成してください。フォルダ名はfeature名とします。（例: `endpoints/<feature_name>/`）。

チェックリスト（実装前に満たすべき項目）
- Python 3.11 を使用すること。
- Functions runtime は v4 を標準とすること。
- ローカル実行ガイド（virtualenv / Functions Core Tools / uvicorn）を repository に含めること。
- シークレットは Key Vault / 環境変数 / Managed Identity で管理すること。
- ロギング（Application Insights）と監視を組み込むこと。
- CI でユニット + 統合テストを実行すること（pytest を推奨）。

設計の「契約」（Inputs / Outputs / 成功基準）
- 入力: HTTP / Timer / Queue で受け取る JSON ペイロード。
- 出力: Queue メッセージ、HTTP POST（外部 API）、ログ、メトリクス。
- 成功: 関数は冪等性を保ち、再試行や DLQ によりメッセージが失われないこと。

主要なベストプラクティス

1) プロジェクト構成
- ルートに `host.json`、テンプレート化された `local.settings.json.template`、`requirements.txt` を置く。
- Azure Functions blueprint を活用する。
- 各 Function は `endpoints/<function_name>/` に 作成することとし、`endpoint.py`にハンドラを作成する。また`__init__.py`ファイルを用意し、blueprintオブジェクトを公開する。共通ロジックはルートに`shared`フォルダを作成し、その中に実装する。function_app.pyは`endpoints/<function_name>/`からFunctionsを登録するだけ、とする。
- テストは `tests/` にまとめ、pytest を使う。小さなユニットと、ダミー API を使った統合テストを用意する。

2) 依存関係と品質保証
- 依存は `requirements.txt` に固定バージョンで記載する（例: `azure-functions==1.x`）。
- 静的解析と整形: `ruff`/`flake8` + `black`、型チェックは `mypy` を推奨。
- GitHub Actions で lint → unit tests → integration tests の順でチェックする。

3) ローカル開発とデバッグ
- Python 仮想環境（venv）を使い、Functions Core Tools (v4) をインストールしてローカル実行する。
- uv は使用しない。
- ダミーの検索 API / メール API は FastAPI 等で用意し、統合テストで使えるようにする。
- 実行例（ローカル）:
```bash
# 仮想環境の作成
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Functions Core Tools を使って起動
func start
```

4) シークレットと認証
- 本番では Managed Identity を第一選択とする。外部 API には Managed Identity や OAuth2 Client Credentials を用いる。
- Key Vault をシークレット保管の中心にする。local では `local.settings.json`（テンプレート）で置換する。

5) ネットワークとセキュリティ
- 社内 API が VNet 内にある場合は Private Endpoint / VNet Integration / API Management を検討する。
- Functions のアウトバウンドは必要に応じて NAT Gateway や Service Endpoint で固定化する。

6) キュー設計（Service Bus vs Storage Queue）
- 高信頼・順序・セッションが必要なら Azure Service Bus を選ぶ。
- 単純なワークキューでコスト削減が最優先なら Azure Storage Queue を選ぶ。
- いずれでもメッセージスキーマは JSON（id, source, created_at, payload, retries 等）で定める。DLQ と再試行ポリシーを設計する。

7) エラーハンドリングと冪等性
- 処理は可能な限り冪等に実装する（外部副作用には request-id を付与する等）。
- 再試行は指数バックオフを採用し、最大試行回数超過で DLQ へ移動する。

8) ロギング、監視、トレーシング
- Application Insights を導入し、関数呼び出し単位でトレースを記録する。
- AOAI 呼び出しなどコストのかかる外部呼び出しはメトリクスを出し、サンプル率やアラートを設定する。

9) AOAI（Azure OpenAI）利用上の注意点
- 最初はモックでプロンプト検証を行い、本番接続時に実トークン制約・料金・レート制限を検証する。
- 機密情報は送信前にマスキングまたは除去する。プロンプトはテンプレート化してレビュー可能にする。

10) テスト戦略
- ユニット: 関数のロジックを isolate して pytest でテスト。
- 統合: ダミー API を起動して Queue をローカル（Azure Storage Emulator / Azurite）で動かし、エンドツーエンドを検証する。

11) CI/CD とデプロイ
- GitHub Actions で lint → test → optional deploy を実行するワークフローを用意する。
- インフラは Bicep または Terraform でコード管理する（PoC は Bicep 推奨だがチームポリシーに従う）。

12) IaC と構成管理
- Key Vault, App Settings, Managed Identity, Service Bus/Storage の接続情報は IaC で管理する。
- 本番環境の設定は GitHub Secrets / Azure Pipeline Variable group 等で安全に渡す。

13) 小さな追加の推奨
- Start/Stop の削除: 長期間使用しないリソースは停止スケジュールを作る。
- コスト監視: AOAI 呼び出し数とトークン使用量を監視してアラート設定。

参考コマンド例（Windows/Mac の zsh 適用）
```bash
# 仮想環境、インストール
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# ローカル Functions 起動
func start

# テスト実行
pytest -q
```

付録: よくあるエッジケース
- メッセージの重複受信: idempotency token を使って重複を検出・無視する。
- AOAI 呼び出しのタイムアウト: タイムアウト時のフェイルファストとフォールバックメッセージを用意する。
- API 認証切れ: リフレッシュロジックまたは Managed Identity によるトークン再取得を実装する。
