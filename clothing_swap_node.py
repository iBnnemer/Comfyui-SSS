def _clamp_image_number(value, image_count, label):
    if value < 1 or value > image_count:
        clamped = max(1, min(value, image_count))
        print(f"[AAClothingSwap] {label}={value} is out of range for image_count={image_count}; using {clamped} instead.")
        return clamped
    return value


class AAClothingSwap:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_count": ("INT", {"default": 2, "min": 1, "max": 16}),
                "person_image_number": ("INT", {"default": 1, "min": 1, "max": 16}),
                "clothing_image_number": ("INT", {"default": 2, "min": 1, "max": 16}),
                "preserve_identity": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "extra_prompt": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build_prompt"
    CATEGORY = "AA"

    def build_prompt(self, image_count, person_image_number, clothing_image_number, preserve_identity, extra_prompt=""):
        person_n = _clamp_image_number(person_image_number, image_count, "person_image_number")
        clothing_n = _clamp_image_number(clothing_image_number, image_count, "clothing_image_number")

        # Mirrors Comfy-Org's own official Qwen 2.1 example prompt almost
        # word for word - a single short sentence works better than a
        # per-image role listing, which just distracts the model.
        prompt = f"Keep the character and pose in <image{person_n}> unchanged, put the outfit from <image{clothing_n}> on the character"
        if preserve_identity:
            prompt += ", preserve the original facial features and body shape"

        if extra_prompt:
            prompt += f", {extra_prompt.strip()}"

        return (prompt,)
