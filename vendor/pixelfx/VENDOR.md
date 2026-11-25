# pixelfx (копия)

- Источник: https://github.com/patch-gg/pixelfx, версия 0.3.1, коммит 5294518ce7c72e48b6100a744596e0acf57f2826, скачано 2026-11-25.
- Лицензия: MIT (`LICENSE`, `NOTICE.md`). Можно в коммерческих играх, в том числе в Steam.
- Убрано из копии: шрифт Patch Pixel (`gallery/fonts` - не MIT, все права у Patch; галерея показывает текст запасным шрифтом), превью-гифки `docs/readme` (11 МБ), `.github`.
- Скилл для Claude Code: `../../.claude/skills/pixelfx/SKILL.md`. Архив для claude.ai: `../../skills-zip/pixelfx.zip`.

## Что положить в игру

Файл `THIRD_PARTY_LICENSES.txt` из этой папки - в папку сборки игры (рядом с exe или в корень браузерной сборки). Писать о pixelfx на странице Steam не нужно.

## Обновить копию

```bash
git clone --depth 1 https://github.com/patch-gg/pixelfx /tmp/pixelfx
# прочитать изменения (LICENSE, NOTICE.md, skills/pixelfx/SKILL.md, tools/) перед заменой
git -C /tmp/pixelfx archive HEAD | tar -x -C vendor/pixelfx && rm -rf vendor/pixelfx/.github vendor/pixelfx/gallery/fonts vendor/pixelfx/docs/readme
```
