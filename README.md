# Comfyui-SSS

Version 1.0.1

Prompt-writing assistant nodes for **Text Encode Qwen Image 2.1**
multi-reference-image edits. None of them touch images directly — you
load and wire your reference images into the Qwen text-encode node
yourself; each node only builds a ready-to-use `prompt` string, using
`<image1>`, `<image2>`, ... to point at the reference image numbers
(the same tag format Qwen's own official example prompts use).

Category in ComfyUI: `AA`.

## Nodes

- **AA Face/Body Composer** — builds a character-sheet style prompt: which image supplies the face, which supplies the body, pose/angle/mood/shot-type presets, skin cleanup, identity/body preservation, head-to-body proportion consistency, an optional plain studio background, and an optional fitted reference outfit.
- **AA Clothing Swap** — puts the clothing from one reference image on the person in another.
- **AA Face Swap** — replaces just the face on a body/pose canvas image.
- **AA Head Swap** — replaces the whole head (face, hair, head shape) on a body/pose canvas image.
- **AA Pose Swap** — the character keeps its own face/identity/body size, but adopts the body pose and face direction from a second reference image; an optional third image supplies clothing.

All of them share `image_count` (how many reference images you're connecting to the Qwen node) plus per-role `..._image_number` fields, and an optional `extra_prompt` free-text field appended at the end.

## Why image numbers instead of descriptions

Qwen's own prompt-rewrite guide recommends pointing at a reference image
by its number rather than describing facial features in words — verbal
descriptions make the model regenerate the face instead of copying it.
These nodes build sentences like *"`<image1>` is the identity anchor..."*
using the same numbering your reference images get once wired into the
Qwen text-encode node's `image1`/`image2`/... inputs.

## Installation

Copy this folder into `ComfyUI/custom_nodes/` and restart ComfyUI.
