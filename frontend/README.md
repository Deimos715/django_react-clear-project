# React + Vite — чистый шаблон

Краткое описание
- Минималистичный шаблон для разработки SPA на React с Vite (HMR), Sass/CSS поддержкой и базовой конфигурацией ESLint.

Требования
- Node.js LTS (рекомендуется >=16)
- npm / yarn / pnpm

Быстрый старт (Linux)
1. Установить зависимости:
   ```bash
   npm install
   ```
2. Запустить режим разработки:
   ```bash
   npm run dev
   ```
3. Создать сборку:
   ```bash
   npm run build
   ```
4. Предпросмотр сборки:
   ```bash
   npm run preview
   ```
5. Запустить линтинг:
   ```bash
   npm run lint
   ```

Структура проекта (пример)
- index.html — HTML-шаблон
- vite.config.js — конфигурация Vite
- package.json — зависимости и скрипты
- src/
  - main.jsx — точка входа приложения
  - App.jsx — корневой компонент
  - components/ — компоненты (Header, Footer, ...)
  - assets/ — статические ресурсы
  - scss/ или css/ — стили

Рекомендуемые скрипты (в package.json)
- dev — запуск Vite в режиме разработки
- build — сборка для продакшена
- preview — локальный просмотр собранного билда
- lint — запуск ESLint
- test — запуск тестов (если добавлены)