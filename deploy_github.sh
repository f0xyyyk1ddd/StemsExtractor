#!/bin/bash

# ===========================================
# 🚀 GitHub Deploy Script for Stems Extractor Pro
# Username: f0xyyyk1ddd
# ===========================================

set -e  # Останавливаться при ошибках

echo "🎵 Stems Extractor Pro - GitHub Deploy Script"
echo "=============================================="

# Конфигурация
GITHUB_USER="f0xyyyk1ddd"
REPO_NAME="StemsExtractor"
REPO_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo ""
echo "📋 Конфигурация:"
echo "   GitHub User: $GITHUB_USER"
echo "   Repository:  $REPO_NAME"
echo "   URL:         $REPO_URL"
echo ""

# Проверка Git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен!"
    exit 1
fi

# Проверка что мы в правильной директории
if [ ! -f "gui.py" ]; then
    echo "❌ Ошибка: Запустите скрипт из папки StemsExtractor"
    exit 1
fi

# Шаг 1: Проверка Git репозитория
echo "📁 Шаг 1: Проверка Git репозитория..."
if [ ! -d ".git" ]; then
    echo "   Инициализация Git..."
    git init
fi
echo "   ✅ Git репозиторий готов"

# Шаг 2: Проверка origin
echo ""
echo "🔗 Шаг 2: Настройка remote origin..."
if git remote | grep -q "origin"; then
    echo "   Remote origin уже существует, обновляем..."
    git remote set-url origin "$REPO_URL"
else
    echo "   Добавляем remote origin..."
    git remote add origin "$REPO_URL"
fi
echo "   ✅ Remote: $REPO_URL"

# Шаг 3: Проверка ветки
echo ""
echo "🌿 Шаг 3: Настройка ветки main..."
git branch -M main
echo "   ✅ Ветка: main"

# Шаг 4: Добавление файлов
echo ""
echo "📦 Шаг 4: Добавление файлов..."
git add .
echo "   ✅ Файлы добавлены"

# Шаг 5: Проверка наличия изменений и коммит
echo ""
echo "💾 Шаг 5: Создание коммита..."
if git diff --cached --quiet; then
    echo "   ℹ️  Нет новых изменений для коммита"
else
    git commit -m "🎉 Initial release v1.0.0 - Stems Extractor Pro"
    echo "   ✅ Коммит создан"
fi

# Шаг 6: Создание тега
echo ""
echo "🏷️  Шаг 6: Создание тега v1.0.0..."
if git tag | grep -q "v1.0.0"; then
    echo "   ℹ️  Тег v1.0.0 уже существует"
else
    git tag -a v1.0.0 -m "Release v1.0.0 - Initial release of Stems Extractor Pro"
    echo "   ✅ Тег v1.0.0 создан"
fi

# Шаг 7: Push на GitHub
echo ""
echo "🚀 Шаг 7: Отправка на GitHub..."
echo ""
echo "⚠️  ВАЖНО: Перед отправкой убедитесь, что:"
echo "   1. Вы создали репозиторий на GitHub: https://github.com/new"
echo "      - Repository name: StemsExtractor"
echo "      - НЕ ставьте галочки на README, .gitignore, LICENSE"
echo "   2. Вы вошли в GitHub через CLI или настроили SSH ключи"
echo ""
read -p "Репозиторий создан на GitHub? (y/n): " confirm

if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    echo ""
    echo "📤 Отправка кода..."
    git push -u origin main
    
    echo ""
    echo "📤 Отправка тега v1.0.0..."
    git push origin v1.0.0
    
    echo ""
    echo "=============================================="
    echo "✅ УСПЕШНО! Проект опубликован на GitHub!"
    echo "=============================================="
    echo ""
    echo "🔗 Ваш репозиторий: https://github.com/${GITHUB_USER}/${REPO_NAME}"
    echo ""
    echo "📋 Следующие шаги:"
    echo "   1. Откройте: https://github.com/${GITHUB_USER}/${REPO_NAME}/releases/new"
    echo "   2. Выберите тег: v1.0.0"
    echo "   3. Заголовок: 🎉 Stems Extractor Pro v1.0.0"
    echo "   4. Нажмите 'Publish release'"
    echo ""
else
    echo ""
    echo "⏸️  Отправка отменена."
    echo ""
    echo "Когда будете готовы, выполните команды вручную:"
    echo ""
    echo "   git push -u origin main"
    echo "   git push origin v1.0.0"
    echo ""
fi

echo "🎵 FOR DJ'S BY DJ'S 🎧"
