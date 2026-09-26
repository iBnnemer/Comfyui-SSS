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

        parts = []

        if image_count > 1:
            for i in range(1, image_count + 1):
                if i == person_n:
                    role = "the person wearing the outfit to be replaced"
                elif i == clothing_n:
                    role = "the clothing reference"
                else:
                    role = "an additional reference, not used in this edit"
                parts.append(f"<image{i}> is {role}")

        parts.append(f"<image{person_n}> is the canvas: keep this person's face, body, pose and background unchanged")
        parts.append(f"take the exact garment/outfit from <image{clothing_n}> and put it on the person in <image{person_n}>")

        if preserve_identity:
            parts.append(f"preserve the exact facial identity and body structure from <image{person_n}>, do not copy the face or body of <image{clothing_n}>")

        if extra_prompt:
            parts.append(extra_prompt)

        prompt = ", ".join(p.strip() for p in parts if p and p.strip())
        return (prompt,)
