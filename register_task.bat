@echo off
echo タスクスケジューラに task2knowledge を登録します

REM バッチファイルの絶対パスを取得
set BATCH_PATH=%~dp0run_task2knowledge.bat
set TASK_NAME=Task2Knowledge

REM タスクを作成（毎分実行する設定）
schtasks /create /tn %TASK_NAME% /tr "%BATCH_PATH%" /sc minute /mo 1 /ru SYSTEM

if %errorlevel% equ 0 (
    echo タスクの登録が完了しました。
    echo タスク名: %TASK_NAME%
    echo 実行間隔: 毎分
) else (
    echo タスクの登録に失敗しました。管理者権限で実行してください。
)

pause