@echo off
setlocal enabledelayedexpansion

REM Windows version of task execution script
REM Set the number of parallel processes (default: 10)
set MAX_PARALLEL_PROCESSES=10
REM Wait interval between processes (seconds)
set WAIT_INTERVAL=3

REM Script path (relative to current directory)
set SCRIPT_PATH=%~dp0task2knowledge.py
REM Base lock file path
set BASE_LOCK_FILE=%TEMP%\task2knowledge

REM Activate conda environment
call conda activate task2knowledge

REM Count running processes
call :count_running_processes
set running_processes=!errorlevel!

REM Launch processes up to the maximum allowed
for /L %%i in (1,1,%MAX_PARALLEL_PROCESSES%) do (
    if %%i GTR %running_processes% (
        call :find_available_slot
        set slot=!errorlevel!
        
        if !slot! NEQ 0 (
            set lock_file=%BASE_LOCK_FILE%_!slot!.lock
            echo !RANDOM! > "!lock_file!"
            
            REM Run Python script in background
            start /b cmd /c "call conda activate task2knowledge && python "!SCRIPT_PATH!" && del "!lock_file!""
            
            REM Wait before starting next process
            timeout /t %WAIT_INTERVAL% /nobreak > nul
        ) else (
            echo No available slots
            exit /b 1
        )
    )
)

exit /b 0

:count_running_processes
setlocal
set count=0

for /L %%i in (1,1,%MAX_PARALLEL_PROCESSES%) do (
    set lock_file=%BASE_LOCK_FILE%_%%i.lock
    if exist "!lock_file!" (
        REM In Windows, we use lock file existence to determine if process is running
        set /a count+=1
    )
)

exit /b %count%

:find_available_slot
setlocal
for /L %%i in (1,1,%MAX_PARALLEL_PROCESSES%) do (
    set lock_file=%BASE_LOCK_FILE%_%%i.lock
    if not exist "!lock_file!" (
        exit /b %%i
    )
)
exit /b 0