# Deployment

Проект деплоится через GitHub Actions: после `git push` в ветку `main` GitHub подключается к серверу по SSH, обновляет код и перезапускает Docker Compose.

## 1. Один раз подготовить сервер

На сервере должны быть установлены `git`, Docker и Docker Compose plugin.

```bash
git clone git@github.com:oksgorshkova-gif/business_bot.git /opt/business_bot
cd /opt/business_bot
cp .env.example .env
nano .env
docker compose up -d --build
```

В `.env` на сервере заполните реальные значения `ADMIN_BOT_TOKEN`, `CLIENT_BOT_TOKEN`, `PASSWORD`, `DB_PASSWORD`, `CALENDAR_ID` и путь к Google service account JSON.

## 2. Добавить SSH-ключ для GitHub Actions

На своем компьютере создайте отдельный ключ для деплоя:

```bash
ssh-keygen -t ed25519 -C "github-actions-business-bot" -f ~/.ssh/business_bot_deploy
```

Публичный ключ добавьте на сервер в `~/.ssh/authorized_keys` пользователя, который будет деплоить проект:

```bash
cat ~/.ssh/business_bot_deploy.pub
```

Приватный ключ понадобится для GitHub secret:

```bash
cat ~/.ssh/business_bot_deploy
```

## 3. Добавить GitHub Secrets

В GitHub откройте `Settings -> Secrets and variables -> Actions -> New repository secret` и добавьте:

| Secret | Значение |
| --- | --- |
| `SERVER_HOST` | IP или домен сервера |
| `SERVER_USER` | SSH-пользователь на сервере |
| `SERVER_PORT` | SSH-порт, обычно `22` |
| `SERVER_SSH_KEY` | приватный ключ `~/.ssh/business_bot_deploy` |
| `DEPLOY_PATH` | путь к проекту на сервере, например `/opt/business_bot` |

## 4. Как обновлять код

Рабочий цикл:

```bash
git add .
git commit -m "Describe change"
git push origin main
```

После `push` откройте вкладку `Actions` в GitHub и проверьте запуск `Deploy`.

## 5. Где держать проект на компьютере

Лучше хранить рабочие проекты не в `Downloads`, а в отдельной папке, например:

```bash
mkdir -p ~/Projects
mv ~/Downloads/business_bot ~/Projects/business_bot
cd ~/Projects/business_bot
```

Если проект уже открыт из другого места, в IDE нужно открыть новую папку `~/Projects/business_bot`.
