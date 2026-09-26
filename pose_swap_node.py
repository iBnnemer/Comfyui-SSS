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

        parts = []
        for i in range(1, image_count + 1):
            if i == char_n:
                role = "the character, whose facial features, identity and body size/proportions must stay unchanged"
            elif i == pose_n:
                role = "the pose reference, providing the body pose and the face's direction/angle only"
            elif use_clothing and i == clothing_n:
                role = "the clothing reference"
            else:
                role = "an additional reference, not used in this edit"
            parts.append(f"<image{i}> is {role}")

        parts.append(f"<image{char_n}> is the canvas: preserve the exact facial features, identity and body size/proportions from <image{char_n}>, do not change them")
        parts.append(f"change the character's pose to match the pose in <image{pose_n}>: adopt the exact body pose and the face's direction/angle from <image{pose_n}>, but do not copy its facial features, identity, clothing or body size")
        parts.append(f"the output shows only one person: the character from <image{char_n}> in this new pose, do not include the person from <image{pose_n}> in the output, do not show two people side by side")

        if use_clothing:
            parts.append(f"take the exact clothing/outfit from <image{clothing_n}> and put it on the character")

        if extra_prompt:
            parts.append(extra_prompt)

        prompt = ", ".join(p.strip() for p in parts if p and p.strip())
        return (prompt,)
