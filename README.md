Стек:
  Python 3.10+
  FastAPI
  Pydantic + SQLAlchemy (async)
  PostgreSQL
  Docker + Docker Compose

Запуск:
```powershell
docker compose up --build
```
(Команду docker compose up --build используем как основной способ запуска)

Swagger UI: http://localhost:8000/docs


API: http://localhost:8000

(Привёл Invoke-RestMethod для POST/PATCH, потому что в PowerShell часто проще избежать проблем с экранированием JSON-кавычек.)


Примеры запросов (Windows / PowerShell) :
Создать видео:

```powershell
$body = @{
video_path    = "/storage/camera1/2024-01-15_10-30-00.mp4"
start_time    = "2024-01-15T10:30:00+07:00"
duration      = "PT1H"
camera_number = 1
location      = "Entrance"
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8000/videos" `
  -ContentType "application/json" `
  -Body $body
```
Получить все видео:

```powershell
curl.exe "http://localhost:8000/videos"
```
Получить видео с фильтрацией:

```powershell
curl.exe "http://localhost:8000/videos?camera_number=1&camera_number=2&status=new&status=transcoded&location=Entrance&location=Exit"
```
Получить видео по ID:

```powershell
curl.exe "http://localhost:8000/videos/1"
```
Обновить статус:

```powershell
Invoke-RestMethod `
-Method Patch `
-Uri "http://localhost:8000/videos/1/status" `
-ContentType "application/json" `
-Body (@{ status = "transcoded" } | ConvertTo-Json)
```
Таблица videos создаётся автоматически при старте приложения
Возможные статусы: new, transcoded, recognized.
duration передаётся в формате ISO 8601
