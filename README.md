# Azure Functions Python 3.11 PoC Template

このリポジトリは、Azure Functions v4 を Python 3.11 で実装するためのプロジェクトテンプレートです。ベストプラクティスに従った構成とローカル開発環境の構築手順が含まれています。

## 📋 要件

- Python 3.11
- Azure Functions Core Tools v4
- Azure CLI（オプション）

## 🚀 ローカル開発環境のセットアップ

### 1. リポジトリのクローンと仮想環境の作成

```bash
# リポジトリをクローン
git clone <repository-url>
cd AzureFunctionsPython

# Python 3.11 仮想環境の作成
python3.11 -m venv .venv

# 仮想環境の有効化 (Linux/Mac)
source .venv/bin/activate

# 仮想環境の有効化 (Windows)
.venv\Scripts\activate
```

### 2. 依存関係のインストール

```bash
# 依存関係をインストール
pip install -r requirements.txt
```

### 3. Azure Functions Core Tools のインストール

#### Linux (Ubuntu/Debian)
```bash
# Microsoft パッケージリポジトリを追加
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'

# Azure Functions Core Tools v4 をインストール
sudo apt-get update
sudo apt-get install azure-functions-core-tools-4
```

#### macOS
```bash
# Homebrew を使用
brew tap azure/functions
brew install azure-functions-core-tools@4
```

#### Windows
```powershell
# Chocolatey を使用
choco install azure-functions-core-tools-4

# または npm を使用
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

### 4. ローカル設定ファイルの準備

```bash
# テンプレートから設定ファイルをコピー
cp local.settings.json.template local.settings.json

# 必要に応じて local.settings.json を編集
```

### 5. Functions アプリケーションの起動

```bash
# Azure Functions を起動
func start

# または開発モードで起動（自動リロード）
func start --python
```

アプリケーションは `http://localhost:7071` で起動します。

## 📡 エンドポイントの確認

### Hello エンドポイント
```bash
# GET リクエスト（クエリパラメータ）
curl "http://localhost:7071/api/hello?name=Azure"

# POST リクエスト（JSON ボディ）
curl -X POST "http://localhost:7071/api/hello" \
  -H "Content-Type: application/json" \
  -d '{"name": "Functions"}'

# パラメータなしのリクエスト
curl "http://localhost:7071/api/hello"
```

## 🧪 テストの実行

### 単体テストの実行
```bash
# 全テストを実行
pytest

# 単体テストのみ実行
pytest -m "not integration"

# 詳細な出力でテストを実行
pytest -v

# カバレッジ付きでテストを実行
pytest --cov=. --cov-report=html
```

### 統合テストの実行
```bash
# 統合テストのみ実行（準備ができている場合）
pytest -m integration
```

## 🔍 コード品質チェック

### リンターと フォーマッター
```bash
# Ruff でリント
ruff check .

# Ruff でフォーマット
ruff format .

# Mypy で型チェック
mypy . --ignore-missing-imports
```

### セキュリティチェック
```bash
# Safety で脆弱性チェック
safety check

# Bandit でセキュリティ問題をチェック
bandit -r .
```

## 📁 プロジェクト構成

```
AzureFunctionsPython/
├── .github/
│   ├── workflows/
│   │   └── ci.yml                    # CI/CD パイプライン
│   └── copilot-instructions.md       # 開発ガイドライン
├── endpoints/                        # 関数エンドポイント
│   └── hello/                        # サンプル HTTP 関数
│       ├── __init__.py              # Blueprint 定義
│       └── endpoint.py              # 関数ハンドラー
├── shared/                          # 共通ユーティリティ
│   ├── __init__.py
│   ├── response_helpers.py          # レスポンス作成ヘルパー
│   └── validators.py                # 入力値検証
├── tests/                           # テストスイート
│   ├── conftest.py                  # テスト設定
│   ├── test_hello.py                # Hello 関数のテスト
│   └── test_shared.py               # 共通機能のテスト
├── .gitignore                       # Git 無視ファイル
├── function_app.py                  # メインアプリケーション
├── host.json                        # Functions ランタイム設定
├── local.settings.json.template     # ローカル設定テンプレート
├── pyproject.toml                   # Python プロジェクト設定
├── requirements.txt                 # Python 依存関係
└── README.md                        # このファイル
```

## 🛠 新しい関数の追加

### 1. エンドポイントディレクトリの作成
```bash
mkdir -p endpoints/my_function
```

### 2. 関数ハンドラーの実装
`endpoints/my_function/endpoint.py`:
```python
import azure.functions as func
import logging

def my_function_handler(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("My function processed a request.")
    # 関数のロジックを実装
    return func.HttpResponse("Hello from my function!")
```

### 3. Blueprint の定義
`endpoints/my_function/__init__.py`:
```python
import azure.functions as func
from .endpoint import my_function_handler

bp = func.Blueprint()

@bp.function_name(name="my_function")
@bp.route(route="my_function", methods=["GET", "POST"])
def my_function(req: func.HttpRequest) -> func.HttpResponse:
    return my_function_handler(req)
```

### 4. メインアプリに登録
`function_app.py` に blueprint を追加:
```python
from endpoints.my_function import bp as my_function_bp
app.register_blueprint(my_function_bp)
```

## 🔐 シークレット管理

### ローカル開発
- `local.settings.json` にシークレットを保存（Git にコミットしない）
- 環境変数での設定も可能

### 本番環境
- Azure Key Vault を使用
- Managed Identity での認証を推奨
- App Settings での環境変数設定

## 📊 監視とロギング

### Application Insights の設定
```python
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

# Application Insights の設定
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string="InstrumentationKey=your-key-here"
))
```

### カスタムメトリクス
```python
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import view as view_module

# カスタムメトリクスの定義と使用
```

## 🔄 CI/CD パイプライン

GitHub Actions ワークフローが以下のステップを実行します：

1. **Lint**: コード品質チェック（ruff, mypy）
2. **Test**: 単体テスト・統合テストの実行
3. **Security**: セキュリティスキャン（safety, bandit）
4. **Validate**: Functions プロジェクト構造の検証

## 🚀 デプロイ

### Azure への手動デプロイ
```bash
# Azure CLI でログイン
az login

# Functions アプリにデプロイ
func azure functionapp publish <app-name>
```

### GitHub Actions でのデプロイ
CI/CD パイプラインでデプロイを自動化することが可能です。詳細は `.github/workflows/ci.yml` を参照してください。

## 🆘 トラブルシューティング

### よくある問題

1. **Python 3.11 が見つからない**
   ```bash
   # pyenv を使用して Python 3.11 をインストール
   pyenv install 3.11.0
   pyenv local 3.11.0
   ```

2. **Functions Core Tools の起動エラー**
   ```bash
   # 依存関係の再インストール
   pip uninstall azure-functions-worker
   pip install azure-functions-worker
   ```

3. **インポートエラー**
   ```bash
   # PYTHONPATH の設定
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

### ログの確認
```bash
# Functions のログを確認
func logs
```

## 📚 参考資料

- [Azure Functions Python 開発者ガイド](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-reference-python)
- [Azure Functions Core Tools](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-run-local)
- [Python 3.11 公式ドキュメント](https://docs.python.org/3.11/)

## 🤝 コントリビューション

プロジェクトへの貢献を歓迎します。変更を行う前に、`.github/copilot-instructions.md` のガイドラインを確認してください。

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下で提供されています。