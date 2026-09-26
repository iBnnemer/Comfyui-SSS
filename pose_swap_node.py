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

        # This exact phrasing (multiple short imperative sentences, "use
        # imageN only as pose reference", listing body parts to follow) is
        # what the user confirmed actually works for pose transfer - our
        # earlier single comma-joined sentence left the head/face direction
        # unchanged even though it named it.
        prompt = (
            f"use <image{char_n}> as the main character and scene. "
            f"change the character's body pose and head/face direction to match the pose shown in <image{pose_n}>. "
            f"use <image{pose_n}> only as pose reference. "
            f"follow the visible positions of the arms, legs, torso, and head."
        )
        if use_clothing:
            prompt += f" put the outfit from <image{clothing_n}> on the character."
        prompt += " preserve the original facial features and body size."

        if extra_prompt:
            prompt += f" {extra_prompt.strip()}"

        return (prompt,)
