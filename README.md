# CI_Compose_Ansible

Репозиторий содержит проект Telegram-бота Prosche с автоматизацией развёртывания с использованием Docker, Docker Compose и Ansible. Также реализован CI Pipeline на GitHub Actions для проверки Python-кода и сборки Docker-образа.

## Project Structure
- main.py - основной файл Telegram-бота.
- db.py - работа с базой данных.
- mailing.py - логика рассылки.
- requirements.txt - зависимости Python.
- Dockerfile - сборка Docker-образа на базе python:3.11-slim.
- docker-compose.yml - конфигурация запуска и управления контейнером.
- ansible/deploy.yml - Ansible Playbook для автоматизации развёртывания приложения.
- .github/workflows/ci.yml - CI Pipeline на GitHub Actions.

## Docker

Для контейнеризации приложения используется Docker.

Dockerfile устанавливает Python 3.11, необходимые зависимости и копирует файлы проекта.
Docker Compose собирает образ и запускает контейнер prosche-bot.
Настроена политика автоматического перезапуска контейнера unless-stopped.

## Ansible

Для автоматизации развёртывания используется Ansible.

ansible/deploy.yml - основной Playbook.
- Проверяет наличие Docker.
- Устанавливает Docker при необходимости.
- Запускает Docker.
- Запускает приложение через Docker Compose.

## Запуск Playbook
`ansible-playbook ansible/deploy.yml --ask-become-pass`

## Проверка контейнера

После выполнения Playbook проверим запущенные контейнеры:

`docker ps`

## CI Pipeline

Для автоматической проверки проекта используется GitHub Actions.

Файл .github/workflows/ci.yml запускает Pipeline при:
- Push в ветку main.
- Pull Request в ветку main.

## Этапы Pipeline
- Checkout repository - получение исходного кода.
- Setup Python - установка Python 3.11.
-Check Python syntax - проверка синтаксиса Python.
- Check Docker Compose - проверка конфигурации Docker Compose.
- Build Docker image - сборка Docker-образа.
- Success - сообщение об успешном прохождении проверок.

Результаты выполнения Pipeline можно посмотреть во вкладке Actions репозитория GitHub.
