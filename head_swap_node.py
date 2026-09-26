def _clamp_image_number(value, image_count, label):
    if value < 1 or value > image_count:
        clamped = max(1, min(value, image_count))
        print(f"[SSSHeadSwap] {label}={value} is out of range for image_count={image_count}; using {clamped} instead.")
        return clamped
    return value


class SSSHeadSwap:
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
    CATEGORY = "SSS"

    def build_prompt(self, image_count, body_image_number, head_image_number, preserve_body, extra_prompt=""):
        body_n = _clamp_image_number(body_image_number, image_count, "body_image_number")
        head_n = _clamp_image_number(head_image_number, image_count, "head_image_number")

        parts = []

        if image_count > 1:
            for i in range(1, image_count + 1):
                if i == body_n:
                    role = "the canvas, whose body, pose and background stay unchanged"
                elif i == head_n:
                    role = "the head reference"
                else:
                    role = "an additional reference, not used in this edit"
                parts.append(f"<image{i}> is {role}")

        parts.append(f"<image{body_n}> is the canvas: keep the body, pose, clothing and background from <image{body_n}> unchanged")
        parts.append(f"replace the entire head, including face, hair and head shape, in <image{body_n}> with the exact head from <image{head_n}>, do not copy <image{head_n}>'s body or clothing")

        if preserve_body:
            parts.append(f"preserve the natural body structure and proportions from <image{body_n}>")

        if extra_prompt:
            parts.append(extra_prompt)

        prompt = ", ".join(p.strip() for p in parts if p and p.strip())
        return (prompt,)
