SHOT_TYPE_PROMPTS = {
    "Portrait": "a portrait shot, framed from the shoulders up",
    "Full Body": "a full-body shot, capturing the entire figure from head to toe",
    "Half Body": "a half-body shot, framed from the waist up",
    "Close-up": "an extreme close-up shot, tightly framed on the face",
    "Wide Shot": "a wide shot, the figure set within a broader scene",
}

FACE_ANGLE_PROMPTS = {
    "Front-facing": "the face photographed front-facing, looking directly at the camera",
    "Three-quarter Left": "the face photographed from a three-quarter angle turned to the left",
    "Three-quarter Right": "the face photographed from a three-quarter angle turned to the right",
    "Profile Left": "the face photographed in left profile",
    "Profile Right": "the face photographed in right profile",
    "Looking Up": "the face tilted upward, photographed looking up",
    "Looking Down": "the face tilted downward, photographed looking down",
}

BODY_POSE_PROMPTS = {
    "Standing Confidently": "standing confidently, shoulders back and head held high",
    "Sitting Relaxed": "sitting relaxed, casual and at ease",
    "Walking Mid-Stride": "walking mid-stride, natural motion captured",
    "Leaning Against a Wall": "leaning casually against a wall",
    "Crouching / Kneeling": "crouching low, one knee bent toward the ground",
    "Arms Crossed": "standing with arms crossed",
    "Looking Over Shoulder": "looking back over the shoulder",
    "Dynamic Action Pose": "a dynamic action pose, mid-motion and full of energy",
    "Lying Down": "lying down, relaxed and at rest",
    "Hands on Hips": "standing with hands on hips, assertive stance",
}

MOOD_PROMPTS = {
    "Joyful": "a joyful expression, bright and cheerful demeanor",
    "Melancholic": "a melancholic expression, quiet sadness in the eyes",
    "Serene / Calm": "a serene, calm expression, peaceful and composed",
    "Intense / Determined": "an intense, determined expression, focused gaze",
    "Mysterious": "a mysterious expression, enigmatic and reserved",
    "Playful": "a playful expression, light-hearted and mischievous",
    "Anxious / Tense": "an anxious, tense expression, visibly on edge",
    "Confident": "a confident expression, self-assured presence",
    "Dreamy / Wistful": "a dreamy, wistful expression, lost in thought",
    "Angry / Fierce": "an angry, fierce expression, sharp and intimidating",
}


def _clamp_image_number(value, image_count, label):
    if value < 1 or value > image_count:
        clamped = max(1, min(value, image_count))
        print(f"[AAFaceBodyComposer] {label}={value} is out of range for image_count={image_count}; using {clamped} instead.")
        return clamped
    return value


class AAFaceBodyComposer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_count": ("INT", {"default": 2, "min": 1, "max": 16}),
                "face_image_number": ("INT", {"default": 1, "min": 1, "max": 16}),
                "body_image_number": ("INT", {"default": 2, "min": 1, "max": 16}),
                "body_pose": (list(BODY_POSE_PROMPTS.keys()), {"default": "Standing Confidently"}),
                "face_angle": (list(FACE_ANGLE_PROMPTS.keys()), {"default": "Front-facing"}),
                "mood": (list(MOOD_PROMPTS.keys()), {"default": "Confident"}),
                "shot_type": (list(SHOT_TYPE_PROMPTS.keys()), {"default": "Portrait"}),
                "clean_face_skin": ("BOOLEAN", {"default": True}),
                "preserve_body_structure": ("BOOLEAN", {"default": True}),
                "proportion_consistency": ("BOOLEAN", {"default": True}),
                "preserve_face_identity": ("BOOLEAN", {"default": True}),
                "neutral_studio_background": ("BOOLEAN", {"default": True}),
                "reference_outfit": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "extra_prompt": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build_prompt"
    CATEGORY = "AA"

    def build_prompt(
        self,
        image_count,
        face_image_number,
        body_image_number,
        body_pose,
        face_angle,
        mood,
        shot_type,
        clean_face_skin,
        preserve_body_structure,
        proportion_consistency,
        preserve_face_identity,
        neutral_studio_background,
        reference_outfit,
        extra_prompt="",
    ):
        face_n = _clamp_image_number(face_image_number, image_count, "face_image_number")
        body_n = _clamp_image_number(body_image_number, image_count, "body_image_number")

        # Kept short and direct, mirroring Comfy-Org's own official Qwen 2.1
        # example prompt - a per-image role listing and long repeated
        # qualifiers distract the model more than they help.
        if face_n == body_n:
            parts = [f"Use the character in <image{face_n}>"]
        else:
            parts = [f"Combine the face from <image{face_n}> with the body from <image{body_n}>"]

        parts.append(SHOT_TYPE_PROMPTS[shot_type])
        parts.append(FACE_ANGLE_PROMPTS[face_angle])
        parts.append(BODY_POSE_PROMPTS[body_pose])
        parts.append(MOOD_PROMPTS[mood])

        if clean_face_skin:
            parts.append("clean face's skin, no acne or blemishes")

        if preserve_face_identity or preserve_body_structure:
            parts.append("preserve the original facial features and body proportions")

        if proportion_consistency:
            parts.append("keep the head-to-body size ratio natural")

        if reference_outfit:
            parts.append("wearing a form-fitting solid-color athletic tank top with matching very short shorts, shoulders exposed")

        if neutral_studio_background:
            parts.append("plain light gray studio background, even natural lighting, no shadow")

        if extra_prompt:
            parts.append(extra_prompt)

        prompt = ", ".join(p.strip() for p in parts if p and p.strip())
        return (prompt,)
