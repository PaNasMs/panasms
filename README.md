# PaNasMs workspace

Полное название — **Pavlo's NAS Management System**, кодовое название — **PaNasMs**, системный идентификатор — `panasms`.
Текущий прототип: **0.2.x**; исходники сохраняются в ветках `main` без нового релизного тега. [Переименование и совместимость](docs/panasms-renaming.md).

Workspace отдельных репозиториев PaNasMs. Основной репозиторий хранит этот обзор, лицензию и общие инструменты; исходники компонентов публикуются отдельно.

| Каталог / репозиторий | Ответственность |
| --- | --- |
| [frontend](https://github.com/PaNasMs/frontend) | React SPA: оболочка, страницы модулей, виджеты, настройки |
| [backend](https://github.com/PaNasMs/backend) | Go core, привилегированный агент, рабочие процессы, API и системная интеграция |
| [docs](https://github.com/PaNasMs/docs) | Требования, архитектура, задачи, документация и история исследований |
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

- [PaNasMs/panasms](https://github.com/PaNasMs/panasms) — workspace overview and shared tools.
- [PaNasMs/backend](https://github.com/PaNasMs/backend) — core, privileged agent and system integration.
- [PaNasMs/frontend](https://github.com/PaNasMs/frontend) — React web interface.
- [PaNasMs/docs](https://github.com/PaNasMs/docs) — project plans and documentation.
- [PaNasMs/module-sdk](https://github.com/PaNasMs/module-sdk) — module SDK.
- [PaNasMs/module-registry](https://github.com/PaNasMs/module-registry) — module catalog.
- [PaNasMs/module-files](https://github.com/PaNasMs/module-files), [module-terminal](https://github.com/PaNasMs/module-terminal), [module-cloud-sync](https://github.com/PaNasMs/module-cloud-sync) — installable modules.

Clone the components into their matching workspace directories to retain existing relative build paths:

```sh
git clone git@github.com:PaNasMs/panasms.git
cd panasms
git clone git@github.com:PaNasMs/backend.git backend
git clone git@github.com:PaNasMs/frontend.git frontend
git clone git@github.com:PaNasMs/docs.git docs
git clone git@github.com:PaNasMs/module-sdk.git module-sdk
git clone git@github.com:PaNasMs/module-registry.git module-registry
git clone git@github.com:PaNasMs/module-files.git modules/files
git clone git@github.com:PaNasMs/module-terminal.git modules/terminal
git clone git@github.com:PaNasMs/module-cloud-sync.git modules/cloud-sync
```

Local credentials, machine configuration snapshots, screenshots, downloaded vendor materials,
build outputs, session notes and chassis CAD are excluded from this source backup.
New core repositories have no automated builds or releases configured.

## Лицензия

Оригинальный программный код PaNasMs — **PolyForm Noncommercial 1.0.0**:
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
