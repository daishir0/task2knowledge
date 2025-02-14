## Overview
task2knowledge is a Python script that processes tasks from the LLMKnowledge2 system database using OpenAI's GPT model. It automatically retrieves pending tasks, processes them using AI, and stores the results as knowledge entries in the database. The script includes features such as text chunking, language detection, and comprehensive logging.

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

3. Set up your environment:
   - Configure the database path in the script (DATABASE_PATH)
   - Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key'
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
- Process text using OpenAI's API
- Save results as knowledge entries
- Log all operations to task2knowledge.log

## Notes
- The script automatically handles text chunking for large content
- Supports both Japanese and English text processing
- Implements retry mechanism for API calls
- Maintains detailed logs in the script's directory
- Requires access to LLMKnowledge2 system database

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

# task2knowledge

## 概要
task2knowledgeは、LLMKnowledge2システムのデータベースからタスクを処理するPythonスクリプトです。OpenAIのGPTモデルを使用して、保留中のタスクを自動的に取得し、AI処理を行い、その結果をナレッジとしてデータベースに保存します。テキストの分割処理、言語検出、包括的なログ機能を備えています。

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

3. 環境を設定します：
   - スクリプト内でデータベースパスを設定 (DATABASE_PATH)
   - OpenAI APIキーを環境変数として設定：
```bash
export OPENAI_API_KEY='your-api-key'
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
- OpenAI APIを使用してテキスト処理
- 結果をナレッジとして保存
- すべての操作をtask2knowledge.logに記録

## 注意点
- 大きなテキストは自動的に適切なサイズに分割して処理
- 日本語と英語のテキスト処理に対応
- API呼び出しの再試行機能を実装
- スクリプトのディレクトリに詳細なログを保持
- LLMKnowledge2システムのデータベースへのアクセスが必要

## ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。詳細はLICENSEファイルを参照してください。
