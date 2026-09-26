# Comfyui-SSS

Version 1.1.0

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
- **AA Pose Swap** — the character keeps its own face/identity/body size, but adopts the body pose from a second reference image; an optional third image supplies clothing.
- **AA Camera Angle from 3D** — takes the `camera_info` output of ComfyUI's native `Load 3D (Advanced)` node and turns it into a `face_angle`-style descriptive sentence, computed from wherever you actually dragged the camera in the 3D viewport (plus raw azimuth/elevation degrees).

All of them share `image_count` (how many reference images you're connecting to the Qwen node) plus per-role `..._image_number` fields, and an optional `extra_prompt` free-text field appended at the end.

## Why image numbers instead of descriptions

Qwen's own prompt-rewrite guide recommends pointing at a reference image
by its number rather than describing facial features in words — verbal
descriptions make the model regenerate the face instead of copying it.
These nodes build sentences like *"`<image1>` is the identity anchor..."*
using the same numbering your reference images get once wired into the
Qwen text-encode node's `image1`/`image2`/... inputs.

## AA Pose Swap: avoiding identity leakage from the pose reference photo

Feeding a real photo of a different person straight in as the pose
reference image and telling the model in the prompt not to copy that
person's face is unreliable — a strong visual cue like a clear face in
the reference image can outrank the instruction, and the output ends up
with the *pose reference's* face instead of your character's.

The reliable fix is to **convert the pose reference photo into a pose
skeleton image first**, and use that skeleton (not the photo) as the
pose reference image. A skeleton has no face, skin, or hair at all, so
there is nothing for identity to leak from.

Your ComfyUI install already has everything needed for this natively,
no extra custom node package required:

```
LoadImage (pose reference photo)
  → SDPoseKeypointExtractor  (needs a checkpoint from
      https://huggingface.co/Comfy-Org/SDPose, ~1.9GB, in models/checkpoints)
  → SDPoseDrawKeypoints      (draw_face=false recommended)
  → this skeleton image is wired as image2 (or whichever number is the
    pose reference) into Text Encode Qwen Image 2.1, instead of the
    original photo
```

`AA Pose Swap`'s prompt already anticipates this — it explicitly says
"do not copy the person, clothing, background, skeleton lines, or joint
markers from `<imageN>`", which only makes sense once that image is a
skeleton render rather than a photo. This has been verified end to end:
the character's own face stays intact while the body adopts the
skeleton's pose.

## Verified working model set (Qwen Image 2.1, `qwen_image_2.1_int8_convrot`)

If you're on the newer quantized Qwen 2.1 release, this is the
combination confirmed to work (not every CLIP file in the picker is
correct for this checkpoint):

- VAE: `qwen_image_2.1_vae_bf16.safetensors`
- CLIP: `qwen3vl_8b_int8_convrot.safetensors` (type: `qwen_image`)
- UNET: `qwen\qwen2\qwen_image_2.1_int8_convrot.safetensors`

## AA Camera Angle from 3D: an interactive camera angle picker

Instead of choosing a fixed angle from a dropdown, you can drag a real
camera around a 3D model and read the exact angle you picked:

1. Add ComfyUI's native **`Load 3D (Advanced)`** node and load any
   humanoid model file (glb/obj/fbx/stl). A free, tiny test model is
   `CesiumMan.glb` from Khronos Group's official glTF-Sample-Models
   repository (CC-BY, ~479KB) — download it into
   `ComfyUI/input/3d/CesiumMan.glb` and it shows up in the node's
   `model_file` picker immediately.
2. Drag inside the node's viewport to orbit the camera around the
   model to whatever angle you want.
3. Wire its `camera_info` output into **`AA Camera Angle from 3D`**.
   Its `angle_description` output is a ready-to-use sentence (e.g.
   *"the face photographed from a three-quarter angle turned to the
   left, the camera is at eye level"*) you can drop into `extra_prompt`
   on any of the other nodes, or use in place of the `face_angle`
   dropdown. `azimuth_degrees`/`elevation_degrees` are also exposed raw.

User-verified: the generated sentence matches the angle picked in the
viewport.

## Installation

Copy this folder into `ComfyUI/custom_nodes/` and restart ComfyUI.
