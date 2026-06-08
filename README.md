# Jiaran-aichifan

A pixel-art custom pet for Codex Desktop, inspired by Jiaran-style chibi character design.

The pet is named **嘉然艾池繁** and includes a 9-state Codex spritesheet with idle blinking, running, waving, failed, waiting, working, and review animations.

## Preview

### Idle

![Idle preview](assets/previews/idle.png)

### Running

![Running right preview](assets/previews/running-right.png)

### Waving

![Waving preview](assets/previews/waving.png)

### Waiting

![Waiting preview](assets/previews/waiting.png)

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
- `assets/spritesheet.png`: source PNG spritesheet, 1536x1872.
- `assets/previews/`: preview strips for key states.
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

## License

Code and packaging metadata are released under the MIT License. Art assets are released under CC BY-NC 4.0; see `LICENSE` for details.
