## Overview
task2knowledge is a Python script that processes tasks from the LLMKnowledge2 system database using various LLM models. It supports both cloud-based LLMs (OpenAI GPT, Anthropic Claude, DeepSeek) and local LLMs (LMStudio, Ollama, vLLM). The script automatically retrieves pending tasks, processes them using AI, and stores the results as knowledge entries in the database.

## Supported LLM Models

### Cloud-based LLMs
- OpenAI: gpt-4o, gpt-4o-mini (default)
- Anthropic: claude-3-5-sonnet-latest, claude-3-5-haiku-latest
- DeepSeek: deepseek-chat, deepseek-reasoner

### Local LLMs
- LMStudio (OpenAI compatible API)
- Ollama
- vLLM (OpenAI compatible API)

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
     - API keys (for cloud-based LLMs)
     - Local LLM endpoints and parameters
     - Your preferred default model

## Configuration
The config.yaml file contains all configurable settings. Here are some example configurations:

### Using Cloud-based LLMs
```yaml
models:
  openai:
    gpt-4o:
      provider: openai
      model_name: gpt-4o
      api_key: your-openai-api-key-here

default_model: gpt-4o
```

### Using LMStudio (Local LLM)
```yaml
models:
  local:
    lmstudio:
      provider: openai_compatible
      model_name: local_model
      endpoint: http://localhost:1234/v1
      api_key: not-needed
      parameters:
        temperature: 0.7
        max_tokens: 4096
        top_p: 0.95

default_model: lmstudio
```

### Using Ollama (Local LLM)
```yaml
models:
  local:
    ollama:
      provider: ollama
      model_name: llama2
      endpoint: http://localhost:11434/api/generate
      parameters:
        temperature: 0.7
        context_length: 4096

default_model: ollama
```

## Local LLM Setup

### Using with LMStudio
1. Install and launch LMStudio
2. Load your preferred model
3. Enable OpenAI compatible API server (default port: 1234)
4. Configure task2knowledge to use LMStudio:
   - Set appropriate endpoint in config.yaml
   - Set default_model to your LMStudio configuration name

### Using with Ollama
1. Install Ollama
2. Pull your preferred model: `ollama pull llama2`
3. Configure task2knowledge to use Ollama:
   - Set appropriate endpoint in config.yaml
   - Set default_model to your Ollama configuration name

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
- Process text using the configured LLM (cloud-based or local)
- Save results as knowledge entries
- Log all operations to task2knowledge.log

## Notes
- The script automatically handles text chunking for large content
- Supports both Japanese and English text processing
- Implements retry mechanism for API calls
- Maintains detailed logs in the script's directory
- Requires access to LLMKnowledge2 system database
- Configuration is externalized in config.yaml
- Supports multiple LLM providers and models (both cloud and local)
- Supports parallel processing through run_task2knowledge.sh

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

# task2knowledge

## 概要
task2knowledgeは、LLMKnowledge2システムのデータベースからタスクを処理するPythonスクリプトです。クラウドベースのLLM（OpenAI GPT、Anthropic Claude、DeepSeek）とローカルLLM（LMStudio、Ollama、vLLM）の両方をサポートし、保留中のタスクを自動的に取得し、AI処理を行い、その結果をナレッジとしてデータベースに保存します。

## 対応LLMモデル

### クラウドベースLLM
- OpenAI: gpt-4o, gpt-4o-mini（デフォルト）
- Anthropic: claude-3-5-sonnet-latest, claude-3-5-haiku-latest
- DeepSeek: deepseek-chat, deepseek-reasoner

### ローカルLLM
- LMStudio（OpenAI互換API）
- Ollama
- vLLM（OpenAI互換API）

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
     - APIキー（クラウドベースLLM用）
     - ローカルLLMのエンドポイントとパラメーター
     - デフォルトのモデル

## 設定
config.yamlファイルには以下のような設定が含まれます：

### クラウドベースLLMを使用する場合
```yaml
models:
  openai:
    gpt-4o:
      provider: openai
      model_name: gpt-4o
      api_key: your-openai-api-key-here

default_model: gpt-4o
```

### LMStudio（ローカルLLM）を使用する場合
```yaml
models:
  local:
    lmstudio:
      provider: openai_compatible
      model_name: local_model
      endpoint: http://localhost:1234/v1
      api_key: not-needed
      parameters:
        temperature: 0.7
        max_tokens: 4096
        top_p: 0.95

default_model: lmstudio
```

### Ollama（ローカルLLM）を使用する場合
```yaml
models:
  local:
    ollama:
      provider: ollama
      model_name: llama2
      endpoint: http://localhost:11434/api/generate
      parameters:
        temperature: 0.7
        context_length: 4096

default_model: ollama
```

## ローカルLLMのセットアップ

### LMStudioを使用する場合
1. LMStudioをインストールして起動
2. 使用したいモデルをロード
3. OpenAI互換APIサーバーを有効化（デフォルトポート：1234）
4. task2knowledgeの設定：
   - config.yamlで適切なエンドポイントを設定
   - default_modelをLMStudioの設定名に設定

### Ollamaを使用する場合
1. Ollamaをインストール
2. 使用したいモデルを取得：`ollama pull llama2`
3. task2knowledgeの設定：
   - config.yamlで適切なエンドポイントを設定
   - default_modelをOllamaの設定名に設定

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
- 設定されたLLM（クラウドまたはローカル）を使用してテキスト処理
- 結果をナレッジとして保存
- すべての操作をtask2knowledge.logに記録

## 注意点
- 大きなテキストは自動的に適切なサイズに分割して処理
- 日本語と英語のテキスト処理に対応
- API呼び出しの再試行機能を実装
- スクリプトのディレクトリに詳細なログを保持
- LLMKnowledge2システムのデータベースへのアクセスが必要
- 設定はconfig.yamlに外部化
- 複数のLLMプロバイダーとモデルに対応（クラウド・ローカル両方）
- run_task2knowledge.shによる並列処理に対応

## ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。詳細はLICENSEファイルを参照してください。
