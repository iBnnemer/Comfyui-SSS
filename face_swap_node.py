def _clamp_image_number(value, image_count, label):
    if value < 1 or value > image_count:
        clamped = max(1, min(value, image_count))
        print(f"[SSSFaceSwap] {label}={value} is out of range for image_count={image_count}; using {clamped} instead.")
        return clamped
    return value


class SSSFaceSwap:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_count": ("INT", {"default": 2, "min": 1, "max": 16}),
                "body_image_number": ("INT", {"default": 1, "min": 1, "max": 16}),
                "face_image_number": ("INT", {"default": 2, "min": 1, "max": 16}),
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

    def build_prompt(self, image_count, body_image_number, face_image_number, preserve_body, extra_prompt=""):
        body_n = _clamp_image_number(body_image_number, image_count, "body_image_number")
        face_n = _clamp_image_number(face_image_number, image_count, "face_image_number")

        parts = []

        if image_count > 1:
            for i in range(1, image_count + 1):
                if i == body_n:
                    role = "the canvas, whose body, pose and background stay unchanged"
                elif i == face_n:
                    role = "the face reference"
                else:
                    role = "an additional reference, not used in this edit"
                parts.append(f"<image{i}> is {role}")

        parts.append(f"<image{body_n}> is the canvas: keep the body, pose, clothing and background from <image{body_n}> unchanged")
        parts.append(f"replace the face in <image{body_n}> with the exact facial features and identity from <image{face_n}>, do not copy <image{face_n}>'s body or clothing")

        if preserve_body:
            parts.append(f"preserve the natural body structure and proportions from <image{body_n}>")

        if extra_prompt:
            parts.append(extra_prompt)

        prompt = ", ".join(p.strip() for p in parts if p and p.strip())
        return (prompt,)
