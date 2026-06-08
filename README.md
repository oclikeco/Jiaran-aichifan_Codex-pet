# Jiaran-aichifan Codex Pet

一个用于 Codex Desktop 的像素风自定义 Pet。角色名为 **嘉然艾池繁**，包含 idle 眨眼、左右跑动、挥手、等待、工作、失败、review 等状态动画。

This is a pixel-art custom pet for Codex Desktop. The pet is named **嘉然艾池繁** and includes a full 8x9 spritesheet for Codex pet states.

## Preview

### Idle

![Idle preview](assets/previews/idle.png)

### Running

![Running right preview](assets/previews/running-right.png)

![Running left preview](assets/previews/running-left.png)

### Waving

![Waving preview](assets/previews/waving.png)

### Waiting

![Waiting preview](assets/previews/waiting.png)

### Review

![Review preview](assets/previews/review.png)

## Install

Copy the `pet` directory into your Codex pets directory:

```bash
mkdir -p ~/.codex/pets/jiaran-aichifan
cp pet/pet.json pet/spritesheet.webp ~/.codex/pets/jiaran-aichifan/
```

Then select **嘉然艾池繁** from Codex Desktop's pet settings. Restart Codex Desktop if the new pet does not appear immediately.

## Files

- `pet/pet.json`: Codex custom pet manifest.
- `pet/spritesheet.webp`: final installed spritesheet.
- `assets/spritesheet.png`: source PNG spritesheet, `1536x1872`.
- `assets/previews/`: preview strips for key states.
- `assets/open-cell.png`: open-eye idle frame.
- `assets/closed-cell.png`: closed-eye idle frame.
- `tools/apply_user_idle_frames.py`: helper script used during asset assembly.

## Spritesheet Layout

The spritesheet is `1536x1872`, arranged as `8` columns by `9` rows. Each frame is `192x208`.

Rows:

1. `idle`
2. `running-right`
3. `running-left`
4. `waving`
5. `jumping` using waving frames
6. `failed`
7. `waiting`
8. `running`
9. `review`

## Copyright And Trademark Notice

This repository is an unofficial, fan-made Codex Desktop pet. It is not affiliated with, endorsed by, sponsored by, or approved by the owners of 嘉然, A-SOUL, or any related character, brand, trademark, or commercial IP.

嘉然 and related names, designs, likenesses, trademarks, and other protected materials belong to their respective rights holders. This project does not claim ownership over those underlying rights.

The included image assets are provided only as a non-commercial fan-made resource for personal use, study, and archival purposes. Do not use these assets for commercial products, paid distribution, advertising, merchandise, or any use that suggests official authorization.

If you are a rights holder and want any material removed or changed, please open an issue or contact the repository owner.

## License

Code, scripts, and packaging metadata are released under the MIT License. Image assets are not covered by the MIT License; see `LICENSE` for the full copyright and asset-use notice.
