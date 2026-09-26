from .composer_node import AAFaceBodyComposer
from .clothing_swap_node import AAClothingSwap
from .face_swap_node import AAFaceSwap
from .head_swap_node import AAHeadSwap
from .pose_swap_node import AAPoseSwap
from .camera_angle_node import AACameraAngleFrom3D

NODE_CLASS_MAPPINGS = {
    "AAFaceBodyComposer": AAFaceBodyComposer,
    "AAClothingSwap": AAClothingSwap,
    "AAFaceSwap": AAFaceSwap,
    "AAHeadSwap": AAHeadSwap,
    "AAPoseSwap": AAPoseSwap,
    "AACameraAngleFrom3D": AACameraAngleFrom3D,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "AAFaceBodyComposer": "AA Face/Body Composer",
    "AAClothingSwap": "AA Clothing Swap",
    "AAFaceSwap": "AA Face Swap",
    "AAHeadSwap": "AA Head Swap",
    "AAPoseSwap": "AA Pose Swap",
    "AACameraAngleFrom3D": "AA Camera Angle from 3D",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
