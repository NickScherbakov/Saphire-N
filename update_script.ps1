$projectPath = "O:\GitHubDown\Saphire-N"
Set-Location -Path $projectPath

Write-Host "Проверка установленных версий библиотек..."
pip show openai httpx

Write-Host "Обновление библиотек openai и httpx..."
pip install --upgrade openai httpx

Write-Host "Переустановка библиотек openai и httpx..."
pip uninstall -y openai httpx
pip install openai httpx

$testFilePath = "test_openai_assistant.py"
$backupFilePath = "test_openai_assistant_backup.py"
Copy-Item -Path $testFilePath -Destination $backupFilePath -Force
Write-Host "Создана резервная копия файла тестов: $backupFilePath"

$testFileContent = Get-Content -Path $testFilePath
$updatedContent = $testFileContent -replace "@patch\('openai_assistant.requests'\)", "@patch('requests.post')"
Set-Content -Path $testFilePath -Value $updatedContent
Write-Host "Файл тестов обновлен."