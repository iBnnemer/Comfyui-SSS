import math


def _azimuth_text(azimuth_deg):
    # 0 deg = camera directly in front of the subject (its default position
    # in the Load3D viewport before you drag anything). Positive angles
    # rotate toward +X; whether that reads as "left" or "right" on screen
    # depends on which way the loaded model is facing, so treat these
    # left/right labels as a starting guess and adjust by eye in the
    # viewport if they're mirrored for your model.
    a = azimuth_deg % 360
    if a > 180:
        a -= 360
    mag = abs(a)
    side = "right" if a > 0 else "left"

    if mag <= 22.5:
        return "the face photographed front-facing, looking directly at the camera"
    if mag <= 67.5:
        return f"the face photographed from a three-quarter angle turned to the {side}"
    if mag <= 112.5:
        return f"the face photographed in {side} profile"
    if mag <= 157.5:
        return f"the face photographed from a three-quarter angle from behind, turned to the {side}"
    return "the face and back of the head photographed from directly behind"


def _elevation_text(elevation_deg):
    if elevation_deg > 15:
        return "the camera is elevated above eye level, looking down at the subject"
    if elevation_deg < -15:
        return "the camera is below eye level, looking up at the subject"
    return "the camera is at eye level"


class AACameraAngleFrom3D:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "camera_info": ("LOAD3D_CAMERA",),
            },
        }

    RETURN_TYPES = ("STRING", "FLOAT", "FLOAT")
    RETURN_NAMES = ("angle_description", "azimuth_degrees", "elevation_degrees")
    FUNCTION = "describe"
    CATEGORY = "AA"

    def describe(self, camera_info):
        position = camera_info["position"]
        target = camera_info["target"]

        dx = position["x"] - target["x"]
        dy = position["y"] - target["y"]
        dz = position["z"] - target["z"]

        horizontal_dist = math.sqrt(dx * dx + dz * dz)
        elevation_deg = math.degrees(math.atan2(dy, horizontal_dist))
        azimuth_deg = math.degrees(math.atan2(dx, dz))

        description = f"{_azimuth_text(azimuth_deg)}, {_elevation_text(elevation_deg)}"
        return (description, azimuth_deg, elevation_deg)
