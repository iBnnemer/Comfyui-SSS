def _clamp_image_number(value, image_count, label):
    if value < 1 or value > image_count:
        clamped = max(1, min(value, image_count))
        print(f"[AAPoseSwap] {label}={value} is out of range for image_count={image_count}; using {clamped} instead.")
        return clamped
    return value


class AAPoseSwap:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_count": ("INT", {"default": 2, "min": 2, "max": 16}),
                "character_image_number": ("INT", {"default": 1, "min": 1, "max": 16}),
                "pose_image_number": ("INT", {"default": 2, "min": 1, "max": 16}),
                "clothing_image_number": ("INT", {"default": 3, "min": 1, "max": 16}),
            },
            "optional": {
                "extra_prompt": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build_prompt"
    CATEGORY = "AA"

    def build_prompt(self, image_count, character_image_number, pose_image_number, clothing_image_number, extra_prompt=""):
        char_n = _clamp_image_number(character_image_number, image_count, "character_image_number")
        pose_n = _clamp_image_number(pose_image_number, image_count, "pose_image_number")
        use_clothing = image_count >= 3
        clothing_n = _clamp_image_number(clothing_image_number, image_count, "clothing_image_number") if use_clothing else None

        # User-verified phrasing (community template): naming the kept
        # attributes explicitly ("face, hairstyle, body proportions...")
        # plus an explicit anti-copy line for the pose image (including
        # "skeleton lines, or joint markers" for when it's an OpenPose-style
        # reference) is what stopped the pose image's own face/head from
        # leaking into the output - our previous version matched head
        # direction correctly but copied image2's actual head.
        keep_attrs = "face, hairstyle, body proportions, and overall visual style" if use_clothing else "face, hairstyle, body proportions, clothing design, and overall visual style"
        prompt = (
            f"use <image{char_n}> as the main character and scene. "
            f"change the character's body pose to match the pose shown in <image{pose_n}>. "
            f"use <image{pose_n}> only as a pose reference. follow the visible positions of the arms, legs, torso, and head. "
            f"keep the character's {keep_attrs} from <image{char_n}>. "
        )
        if use_clothing:
            prompt += f"put the outfit from <image{clothing_n}> on the character. "
        prompt += (
            f"show one complete character in one continuous image. "
            f"do not copy the person, clothing, background, skeleton lines, or joint markers from <image{pose_n}>."
        )

        if extra_prompt:
            prompt += f" {extra_prompt.strip()}"

        return (prompt,)
