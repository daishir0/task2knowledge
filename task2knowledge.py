import sqlite3
import openai
import anthropic
import datetime
import os
import time
import re
import logging
import yaml
from logging.handlers import RotatingFileHandler

# スクリプトの場所を取得
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 設定ファイルを読み込む
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.yaml")
with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

# 設定から値を取得
DATABASE_PATH = config['database']['path']
CHUNK_SIZE = config['parameters']['chunk_size']
MAX_CHUNK_SIZE = config['parameters']['max_chunk_size']
MAX_RETRIES = config['parameters']['max_retries']
RETRY_DELAY = config['parameters']['retry_delay']
API_RATE_LIMIT = config['parameters']['api_rate_limit']
DEBUG_MODE = config['parameters']['debug_mode']
DEFAULT_MODEL = config['default_model']

# ログファイルの設定
LOG_FILE = os.path.join(SCRIPT_DIR, "task2knowledge.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def debug_print(message):
    """デバッグメッセージを出力"""
    if DEBUG_MODE:
        logger.debug(message)

# 言語依存の設定
SENTENCE_ENDINGS = {
    'ja': ['。', '！', '？'],
    'en': ['.', '!', '?']
}
PARAGRAPH_BREAKS = ['\n\n', '\r\n\r\n']

# 括弧の定義
BRACKETS = {
    'open': ['「', '『', '（', '(', '［', '[', '｛', '{'],
    'close': ['」', '』', '）', ')', '］', ']', '｝', '}']
}

def detect_language(text):
    """テキストの主要言語を検出する"""
    logger.debug("Detecting language...")
    if re.search(r'[ぁ-んァ-ン一-龥]', text):
        logger.debug("Detected language: Japanese")
        return 'ja'
    logger.debug("Detected language: English")
    return 'en'

def is_real_sentence_ending(text, pos, ending):
    """本当の文末かどうかを判断する"""
    if pos + len(ending) >= len(text):
        return True
        
    # 次の文字が開始括弧類でない
    next_char = text[pos + len(ending):pos + len(ending) + 1]
    if next_char in BRACKETS['open']:
        return False
        
    # 省略記号でない
    if ending == '.' and pos + 3 <= len(text):
        if text[pos:pos + 3] == '...':
            return False
            
    # 括弧内の文末でない
    stack = []
    for i in range(pos):
        if text[i] in BRACKETS['open']:
            stack.append(text[i])
        elif text[i] in BRACKETS['close']:
            if stack and BRACKETS['open'].index(stack[-1]) == BRACKETS['close'].index(text[i]):
                stack.pop()
                
    return len(stack) == 0  # 括弧が閉じている場合のみTrue

def find_next_sentence_end(text, start, language, max_end):
    """指定された開始位置から次の文末を探す"""
    endings = SENTENCE_ENDINGS[language]
    
    for i in range(start, min(max_end, len(text))):
        for ending in endings:
            if text[i:i+len(ending)] == ending:
                # 文末の妥当性をチェック
                if is_real_sentence_ending(text, i, ending):
                    return i + len(ending)
    
    return None

def split_text(text, min_chunk_size=CHUNK_SIZE, max_chunk_size=MAX_CHUNK_SIZE):
    """テキストを適切なサイズに分割する改良版"""
    logger.debug("Starting advanced text splitting...")
    logger.debug(f"Text length: {len(text)}")
    
    if len(text) <= min_chunk_size:
        logger.debug("Text is smaller than minimum chunk size, returning as is")
        return [text]

    language = detect_language(text)
    
    chunks = []
    start = 0

    while start < len(text):
        logger.debug(f"Processing chunk starting at position {start}")
        
        # 最小チャンクサイズ以降の文末を探す
        chunk_end = find_next_sentence_end(
            text, 
            start + min_chunk_size, 
            language, 
            min(start + max_chunk_size, len(text))
        )
        
        # 文末が見つからない場合は最大チャンクサイズまでで区切る
        if chunk_end is None:
            chunk_end = min(start + max_chunk_size, len(text))
        
        # チャンクを作成
        chunk = text[start:chunk_end]
        chunks.append(chunk)
        
        # デバッグ情報
        logger.debug(f"Chunk created: {len(chunk)} characters")
        logger.debug(f"Chunk start: {start}, Chunk end: {chunk_end}")
        
        # 次の開始位置を設定
        start = chunk_end
    
    logger.debug(f"Split text into {len(chunks)} chunks")
    return chunks

class LLMClient:
    """LLMクライアントの基底クラス"""
    def __init__(self, model_config):
        self.model_config = model_config
        self.api_key = os.environ.get(model_config['api_key_env'])
        if not self.api_key:
            raise ValueError(f"API key not found in environment: {model_config['api_key_env']}")

    def call_api(self, prompt, text):
        raise NotImplementedError("Subclasses must implement call_api method")

class OpenAIClient(LLMClient):
    """OpenAI APIクライアント"""
    def __init__(self, model_config):
        super().__init__(model_config)
        self.client = openai.OpenAI(api_key=self.api_key)

    def call_api(self, prompt, text):
        request_content = f"{prompt}\n\n{text}"
        completion = self.client.chat.completions.create(
            model=self.model_config['model_name'],
            messages=[
                {"role": "user", "content": request_content}
            ]
        )
        return completion.choices[0].message.content

class AnthropicClient(LLMClient):
    """Anthropic APIクライアント"""
    def __init__(self, model_config):
        super().__init__(model_config)
        self.client = anthropic.Client(api_key=self.api_key)

    def call_api(self, prompt, text):
        request_content = f"{prompt}\n\n{text}"
        message = self.client.messages.create(
            model=self.model_config['model_name'],
            messages=[{
                "role": "user",
                "content": request_content
            }]
        )
        return message.content

class DeepSeekClient(LLMClient):
    """DeepSeek APIクライアント"""
    def __init__(self, model_config):
        super().__init__(model_config)
        self.client = deepseek.Client(api_key=self.api_key)

    def call_api(self, prompt, text):
        request_content = f"{prompt}\n\n{text}"
        response = self.client.chat.completions.create(
            model=self.model_config['model_name'],
            messages=[{
                "role": "user",
                "content": request_content
            }]
        )
        return response.choices[0].message.content

def get_llm_client(model_name=None):
    """LLMクライアントを取得する"""
    if model_name is None:
        model_name = DEFAULT_MODEL

    # モデル設定を探す
    model_config = None
    provider = None
    for p, models in config['models'].items():
        if model_name in models:
            model_config = models[model_name]
            provider = p
            break

    if model_config is None:
        raise ValueError(f"Model configuration not found for: {model_name}")

    # プロバイダに応じたクライアントを返す
    if provider == 'openai':
        return OpenAIClient(model_config)
    elif provider == 'anthropic':
        return AnthropicClient(model_config)
    elif provider == 'deepseek':
        return DeepSeekClient(model_config)
    else:
        raise ValueError(f"Unknown provider: {provider}")

def call_llm_api(client, prompt, text, retries=MAX_RETRIES):
    """LLM APIを呼び出す（リトライ機能付き）"""
    logger.debug("Preparing API request...")
    logger.info("\n=== API Request ===")
    logger.info(f"{prompt}\n\n{text}")
    logger.info("==================")

    for attempt in range(retries):
        try:
            logger.debug(f"Attempt {attempt + 1} of {retries}")
            response = client.call_api(prompt, text)
            logger.debug("API request successful")
            logger.info("\n=== API Response ===")
            logger.info(response)
            logger.info("===================")
            return response
        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            if attempt == retries - 1:
                raise e
            time.sleep(RETRY_DELAY * (attempt + 1))
    return None

def update_task_status(cursor, task_id, status, error_message=None, result_knowledge_id=None):
    """タスクのステータスを更新する"""
    logger.debug(f"Updating task {task_id} status to {status}")
    if status == 'error' and error_message:
        cursor.execute("""
            UPDATE tasks 
            SET status = ?,
                error_message = ?
            WHERE id = ?
        """, (status, error_message, task_id))
    elif status == 'completed' and result_knowledge_id:
        cursor.execute("""
            UPDATE tasks 
            SET status = ?,
                result_knowledge_id = ?
            WHERE id = ?
        """, (status, result_knowledge_id, task_id))
    else:
        cursor.execute("""
            UPDATE tasks 
            SET status = ?
            WHERE id = ?
        """, (status, task_id))
    logger.debug("Task status updated")

def log_knowledge_history(cursor, knowledge_id, data):
    """knowledgeの履歴を記録する関数
    
    Args:
        cursor: データベースカーソル
        knowledge_id: 対象のknowledgeのID
        data: 記録するデータ（title, question, answer, reference）
    """
    logger.debug(f"Logging history for knowledge ID: {knowledge_id}")
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute("""
        INSERT INTO knowledge_history (
            knowledge_id, title, question, answer, reference,
            modified_by, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        knowledge_id,
        data['title'],
        data['question'],
        data['answer'],
        data.get('reference', ''),  # referenceは任意
        'system',
        timestamp
    ))
    logger.debug("History logged successfully")

def main():
    logger.debug("Initializing LLM client")
    # LLMクライアントを初期化
    client = get_llm_client()

    logger.debug("Connecting to database")
    # SQLiteデータベースに接続
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        logger.debug("Fetching pending/processing task")
        # pendingのタスクを1件取得（プロンプトIDも含める）
        cursor.execute("""
            SELECT t.id, t.source_type, t.source_id, t.prompt_content, t.source_text, t.prompt_id as prompt_id, t.status, t.group_id
            FROM tasks t
            WHERE t.status = 'pending'
            ORDER BY
                t.created_at
            LIMIT 1
        """)
        task = cursor.fetchone()

        if task:
            task_id, source_type, source_id, prompt_content, source_text, prompt_id, current_status, group_id = task
            logger.info(f"Processing task ID: {task_id}")
            logger.info(f"Source Type: {source_type}")
            logger.info(f"Current Status: {current_status}")
            logger.info(f"Prompt Content: {prompt_content}")
            logger.info(f"Source Text: {source_text}")
            logger.info(f"Prompt ID: {prompt_id}")

            logger.debug("Checking if task needs status update")
            # タスクのステータスを処理中に更新（まだpendingの場合のみ）
            if current_status == 'pending':
                update_task_status(cursor, task_id, 'processing')
                conn.commit()
                logger.debug("Task status updated to processing")

            logger.debug("Starting text splitting")
            # テキストを分割
            text_chunks = split_text(source_text)
            logger.info(f"\n=== Split into {len(text_chunks)} chunks ===")
            for i, chunk in enumerate(text_chunks, 1):
                logger.info(f"\nChunk {i}/{len(text_chunks)}:")
                logger.info(chunk)
                logger.info("=" * 50)

            logger.debug("Processing chunks")
            all_responses = []

            # 各チャンクを処理
            for i, chunk in enumerate(text_chunks):
                logger.debug(f"Processing chunk {i+1}/{len(text_chunks)}")
                logger.info(f"\nProcessing chunk {i+1}/{len(text_chunks)}")
                
                try:
                    # APIを呼び出し
                    response = call_llm_api(client, prompt_content, chunk)
                    if response:
                        all_responses.append(response)
                    
                    # レートリミット対策
                    if i < len(text_chunks) - 1:
                        logger.debug(f"Waiting {API_RATE_LIMIT} seconds before next chunk")
                        time.sleep(API_RATE_LIMIT)
                except Exception as e:
                    logger.error(f"Error processing chunk {i+1}: {str(e)}")
                    continue

            if not all_responses:
                logger.error("No successful responses from API")
                raise Exception("No successful responses from API")

            logger.debug("Combining responses")
            # 全ての応答を結合
            answer = "\n\n".join(all_responses)
            logger.info("\n=== Final Combined Response ===")
            logger.info(answer)
            logger.info("=============================")

            logger.debug("Fetching source reference")
            # ソースタイプに応じてreferenceを取得
            if source_type == 'record':
                cursor.execute("SELECT title, reference FROM record WHERE id = ?", (source_id,))
                parent_type = 'record'
                question = "(プレーンナレッジからの作成)"
            elif source_type == 'knowledge':
                cursor.execute("SELECT title, reference FROM knowledge WHERE id = ?", (source_id,))
                parent_type = 'knowledge'
                question = "(ナレッジからの作成)"
            else:
                logger.error(f"Invalid source type: {source_type}")
                raise Exception(f"Invalid source type: {source_type}")

            record = cursor.fetchone()
            if not record:
                logger.error(f"Source not found for ID: {source_id}")
                raise Exception(f"Source not found for ID: {source_id}")

            title = record[0]
            reference = record[1] or ""  # referenceがNULLの場合は空文字列を使用
            current_time = datetime.datetime.now()

            logger.debug("Inserting knowledge")
            # knowledgeテーブルにデータを挿入（referenceも含める）
            cursor.execute("""
                INSERT INTO knowledge (
                    title,
                    question,
                    answer,
                    reference,
                    parent_id,
                    parent_type,
                    prompt_id,
                    group_id,
                    created_by,
                    created_at,
                    updated_at,
                    deleted
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'admin', ?, ?, 0)
            """, (
                title,                          # タイトル（ソースから）
                question,                       # 質問（ソースタイプに応じて変更）
                answer,                         # 回答（AI応答）
                reference,                      # 参照情報（ソースから）
                source_id,                      # 親ID
                parent_type,                    # 親タイプ（動的）
                prompt_id,                      # プロンプトID
                group_id,                       # グループID（タスクから）
                current_time,                   # 作成日時
                current_time                    # 更新日時
            ))

            # 新しく挿入されたknowledgeのIDを取得
            knowledge_id = cursor.lastrowid
            
            # 履歴を記録
            history_data = {
                'title': title,
                'question': question,
                'answer': answer,
                'reference': reference
            }
            log_knowledge_history(cursor, knowledge_id, history_data)

            logger.debug("Updating task status to completed")
            # タスクのステータスを完了に更新
            update_task_status(cursor, task_id, 'completed', result_knowledge_id=knowledge_id)
            conn.commit()
            logger.info(f"Knowledge created successfully with ID: {knowledge_id}")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        # エラーメッセージをtasksテーブルに保存
        if 'task_id' in locals():
            update_task_status(cursor, task_id, 'failed', error_message=str(e))
            conn.commit()

    finally:
        logger.debug("Closing database connection")
        conn.close()

if __name__ == "__main__":
    main()