## Overview
task2knowledge is a Python script that processes tasks from the LLMKnowledge2 system database using various LLM models (OpenAI GPT, Anthropic Claude, DeepSeek). It automatically retrieves pending tasks, processes them using AI, and stores the results as knowledge entries in the database. The script includes features such as text chunking, language detection, and comprehensive logging.

## Supported LLM Models
- OpenAI: gpt-4o, gpt-4o-mini (default)
- Anthropic: claude-3-5-sonnet-latest, claude-3-5-haiku-latest
- DeepSeek: deepseek-chat, deepseek-reasoner

## Installation
1. Clone the repository:
```bash
git clone https://github.com/daishir0/task2knowledge.git
cd task2knowledge
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your configuration:
   - Copy the sample configuration file:
   ```bash
   cp config.sample.yaml config.yaml
   ```
   - Edit config.yaml to set:
     - Database path
     - Basic parameters
     - API keys for your LLM models
     - Your preferred default model

## Configuration
The config.yaml file contains all configurable settings:

```yaml
# Database settings
database:
  path: /path/to/your/database.db

# Basic parameters
parameters:
  chunk_size: 2000        # Minimum characters per chunk
  max_chunk_size: 3000    # Maximum characters per chunk
  max_retries: 5          # API retry count
  retry_delay: 5          # Retry interval (seconds)
  api_rate_limit: 0.5     # API call interval (seconds)
  debug_mode: false       # Debug mode toggle

# LLM model settings
models:
  openai:
    gpt-4o:
      provider: openai
      model_name: gpt-4o
      api_key: your-openai-api-key-here
    gpt-4o-mini:
      provider: openai
      model_name: gpt-4o-mini
      api_key: your-openai-api-key-here
  # ... other models

# Default model setting
default_model: gpt-4o-mini
```

## Usage
1. Run the script directly:
```bash
python task2knowledge.py
```

2. For automated execution, use the provided shell script with cron:
```bash
# Edit crontab
crontab -e

# Add a line like this to run every 5 minutes
*/5 * * * * /path/to/run_task2knowledge.sh
```

The script will:
- Fetch pending tasks from the database
- Process text using the configured LLM model
- Save results as knowledge entries
- Log all operations to task2knowledge.log

## Notes
- The script automatically handles text chunking for large content
- Supports both Japanese and English text processing
- Implements retry mechanism for API calls
- Maintains detailed logs in the script's directory
- Requires access to LLMKnowledge2 system database
- Configuration is now externalized in config.yaml
- Supports multiple LLM providers and models
- Supports parallel processing through run_task2knowledge.sh

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

# task2knowledge

## 概要
task2knowledgeは、LLMKnowledge2システムのデータベースからタスクを処理するPythonスクリプトです。OpenAI GPT、Anthropic Claude、DeepSeekなど、様々なLLMモデルを使用して、保留中のタスクを自動的に取得し、AI処理を行い、その結果をナレッジとしてデータベースに保存します。テキストの分割処理、言語検出、包括的なログ機能を備えています。

## 対応LLMモデル
- OpenAI: gpt-4o, gpt-4o-mini（デフォルト）
- Anthropic: claude-3-5-sonnet-latest, claude-3-5-haiku-latest
- DeepSeek: deepseek-chat, deepseek-reasoner

## インストール方法
1. レポジトリをクローンします：
```bash
git clone https://github.com/daishir0/task2knowledge.git
cd task2knowledge
```

2. 必要なパッケージをインストールします：
```bash
pip install -r requirements.txt
```

3. 設定を行います：
   - サンプル設定ファイルをコピーします：
   ```bash
   cp config.sample.yaml config.yaml
   ```
   - config.yamlを編集して以下を設定します：
     - データベースパス
     - 基本パラメーター
     - 使用するLLMモデルのAPIキー
     - デフォルトのモデル

## 設定
config.yamlファイルには以下の設定が含まれています：

```yaml
# データベース設定
database:
  path: /path/to/your/database.db

# 基本パラメーター
parameters:
  chunk_size: 2000        # 1チャンクの最小文字数
  max_chunk_size: 3000    # 1チャンクの最大文字数
  max_retries: 5          # APIリトライ回数
  retry_delay: 5          # リトライ間隔（秒）
  api_rate_limit: 0.5     # API呼び出し間隔（秒）
  debug_mode: false       # デバッグモードの有効無効

# LLMモデル設定
models:
  openai:
    gpt-4o:
      provider: openai
      model_name: gpt-4o
      api_key: your-openai-api-key-here
    gpt-4o-mini:
      provider: openai
      model_name: gpt-4o-mini
      api_key: your-openai-api-key-here
  # ... その他のモデル

# デフォルトモデル設定
default_model: gpt-4o-mini
```

## 使い方
1. スクリプトを直接実行：
```bash
python task2knowledge.py
```

2. 自動実行のため、提供されているシェルスクリプトをcronで使用：
```bash
# crontabを編集
crontab -e

# 5分ごとに実行する場合、以下のような行を追加
*/5 * * * * /path/to/run_task2knowledge.sh
```

スクリプトは以下の処理を行います：
- データベースから保留中のタスクを取得
- 設定されたLLMモデルを使用してテキスト処理
- 結果をナレッジとして保存
- すべての操作をtask2knowledge.logに記録

## 注意点
- 大きなテキストは自動的に適切なサイズに分割して処理
- 日本語と英語のテキスト処理に対応
- API呼び出しの再試行機能を実装
- スクリプトのディレクトリに詳細なログを保持
- LLMKnowledge2システムのデータベースへのアクセスが必要
- 設定はconfig.yamlに外部化
- 複数のLLMプロバイダーとモデルに対応
- run_task2knowledge.shによる並列処理に対応

## ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。詳細はLICENSEファイルを参照してください。
