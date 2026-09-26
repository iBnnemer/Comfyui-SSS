def _clamp_image_number(value, image_count, label):
    if value < 1 or value > image_count:
        clamped = max(1, min(value, image_count))
        print(f"[AAHeadSwap] {label}={value} is out of range for image_count={image_count}; using {clamped} instead.")
        return clamped
    return value


class AAHeadSwap:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_count": ("INT", {"default": 2, "min": 1, "max": 16}),
                "body_image_number": ("INT", {"default": 1, "min": 1, "max": 16}),
                "head_image_number": ("INT", {"default": 2, "min": 1, "max": 16}),
                "preserve_body": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "extra_prompt": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build_prompt"
    CATEGORY = "AA"

    def build_prompt(self, image_count, body_image_number, head_image_number, preserve_body, extra_prompt=""):
        body_n = _clamp_image_number(body_image_number, image_count, "body_image_number")
        head_n = _clamp_image_number(head_image_number, image_count, "head_image_number")

        # Single short sentence, same shape as Comfy-Org's own official
        # Qwen 2.1 example prompt - keeps the model focused instead of
        # scattering its attention over a long per-image role listing.
        prompt = f"Keep the pose, clothing and background in <image{body_n}> unchanged, replace the head with the head from <image{head_n}>"
        if preserve_body:
            prompt += ", preserve the original body shape"

        if extra_prompt:
            prompt += f", {extra_prompt.strip()}"

        return (prompt,)
