@echo off
echo �^�X�N�X�P�W���[���� task2knowledge ��o�^���܂�

REM �o�b�`�t�@�C���̐�΃p�X���擾
set BATCH_PATH=%~dp0run_task2knowledge.bat
set TASK_NAME=Task2Knowledge

REM �^�X�N���쐬�i�������s����ݒ�j
schtasks /create /tn %TASK_NAME% /tr "%BATCH_PATH%" /sc minute /mo 1 /ru SYSTEM

if %errorlevel% equ 0 (
    echo �^�X�N�̓o�^���������܂����B
    echo �^�X�N��: %TASK_NAME%
    echo ���s�Ԋu: ����
) else (
    echo �^�X�N�̓o�^�Ɏ��s���܂����B�Ǘ��Ҍ����Ŏ��s���Ă��������B
)

pause