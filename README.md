# OstojaOS workspace

Название проекта — **OstojaOS**, системный идентификатор — `ostojaos`.
Текущий прототип: **0.2.x**; исходники сохраняются в ветках `main` без нового релизного тега. [Переименование и совместимость](docs/ostojaos-renaming.md).

Workspace отдельных репозиториев OstojaOS. Основной репозиторий хранит этот обзор, лицензию и общие инструменты; исходники компонентов публикуются отдельно.

| Каталог / репозиторий | Ответственность |
| --- | --- |
| [frontend](https://github.com/OstojaOS/frontend) | React SPA: оболочка, страницы модулей, виджеты, настройки |
| [backend](https://github.com/OstojaOS/backend) | Go core, привилегированный агент, рабочие процессы, API и системная интеграция |
| [docs](https://github.com/OstojaOS/docs) | Требования, архитектура, задачи, документация и история исследований |
| `chassis` (локально) | Конструкция корпуса, CAD и материалы изготовления |

Core и агент выпускаются из одного backend-репозитория, но работают
отдельными процессами с разными полномочиями. Файловый менеджер и терминал находятся в `modules/` и выпускаются отдельными
подписанными пакетами с собственными версиями.

План: [решения](docs/custom-nas-project-plan.md),
[задачи реализации](docs/implementation-tasks.md).

## Остальные каталоги

- `scripts/`, `patches/` — исторические инструменты и патчи CasaOS/устройства.
  Они сохранены на прежних путях для совместимости документации и не входят
  автоматически в новую платформу. Нужные части переносить в backend
  осознанно при реализации соответствующего адаптера.
- `tmp/` — временные материалы, не будущий репозиторий.
- `codex-session` — ссылка на внешнюю историю работы, не исходники продукта.
- `.SynologyWorkingDirectory/` — служебные данные синхронизации.

## GitHub repositories

- [OstojaOS/ostojaos](https://github.com/OstojaOS/ostojaos) — workspace overview and shared tools.
- [OstojaOS/backend](https://github.com/OstojaOS/backend) — core, privileged agent and system integration.
- [OstojaOS/frontend](https://github.com/OstojaOS/frontend) — React web interface.
- [OstojaOS/docs](https://github.com/OstojaOS/docs) — project plans and documentation.
- [OstojaOS/module-sdk](https://github.com/OstojaOS/module-sdk) — module SDK.
- [OstojaOS/module-registry](https://github.com/OstojaOS/module-registry) — module catalog.
- [OstojaOS/module-files](https://github.com/OstojaOS/module-files), [module-terminal](https://github.com/OstojaOS/module-terminal), [module-cloud-sync](https://github.com/OstojaOS/module-cloud-sync) — installable modules.

Clone the components into their matching workspace directories to retain existing relative build paths:

```sh
git clone git@github.com:OstojaOS/ostojaos.git
cd ostojaos
git clone git@github.com:OstojaOS/backend.git backend
git clone git@github.com:OstojaOS/frontend.git frontend
git clone git@github.com:OstojaOS/docs.git docs
git clone git@github.com:OstojaOS/module-sdk.git module-sdk
git clone git@github.com:OstojaOS/module-registry.git module-registry
git clone git@github.com:OstojaOS/module-files.git modules/files
git clone git@github.com:OstojaOS/module-terminal.git modules/terminal
git clone git@github.com:OstojaOS/module-cloud-sync.git modules/cloud-sync
```

Local credentials, machine configuration snapshots, screenshots, downloaded vendor materials,
build outputs, session notes and chassis CAD are excluded from this source backup.
New core repositories have no automated builds or releases configured.

## Лицензия

Оригинальный программный код OstojaOS — **PolyForm Noncommercial 1.0.0**:
[полный текст](LICENSE), [область применения и уведомления](NOTICE).
SPDX: `PolyForm-Noncommercial-1.0.0`.

Это проект с публичными исходниками (source available), а не Open Source
в смысле определения OSI. Разрешённые цели использования определяет текст
лицензии, включая его положения об отдельных категориях организаций.
Коммерческое использование за пределами этих разрешений требует отдельной
лицензии правообладателей; готовая коммерческая лицензия пока не предоставляется.

Условия применяются к нашему коду ядра, интерфейса и официальных модулей.
Сторонние компоненты сохраняют свои лицензии. Исторические патчи CasaOS,
чужие материалы, документация производителей и CAD не перелицензируются.
При разделении каталогов на репозитории сохраняем их `LICENSE` и `NOTICE`.
