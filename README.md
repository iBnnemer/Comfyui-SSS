# Comfyui-SSS

ComfyUI custom nodes.

## SSS Face/Body Composer

A prompt-writing assistant node for multi-reference-image editing with
**Text Encode Qwen Image 2.1** (or Qwen-Image-Edit-Plus style nodes). It
has no image inputs/outputs — you load and wire your reference images
directly into the Qwen text-encode node yourself; this node only builds
the `prompt` string.

Category in ComfyUI: `SSS`.

### Inputs

- `image_count` — how many reference images you're connecting to the Qwen node (used to validate the numbers below).
- `face_image_number` / `body_image_number` — which reference image (by number) supplies the face and which supplies the body.
- `body_pose`, `face_angle`, `mood`, `shot_type` — dropdown presets describing the target image.
- `clean_face_skin` — clears acne/blemishes from the face in the prompt.
- `preserve_body_structure`, `preserve_face_identity` — keep the natural body structure / facial identity from their respective reference images.
- `proportion_consistency` — asks for a natural head-to-body size ratio (no oversized head on a small body or vice versa).
- `extra_prompt` (optional) — free text appended at the end.

### Output

- `prompt` (STRING) — connect to the `prompt` input of `Text Encode Qwen Image 2.1`.

### Why image numbers instead of descriptions

Qwen's own prompt-rewrite guide recommends pointing at a reference image
by its number rather than describing facial features in words — verbal
descriptions make the model regenerate the face instead of copying it.
This node builds sentences like *"image 1 is the identity anchor..."*
using the same image numbering your reference images will have once
wired into the Qwen text-encode node.

## Installation

Copy this folder into `ComfyUI/custom_nodes/` and restart ComfyUI.
