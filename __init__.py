from .composer_node import SSSFaceBodyComposer
from .clothing_swap_node import SSSClothingSwap
from .face_swap_node import SSSFaceSwap
from .head_swap_node import SSSHeadSwap
from .pose_swap_node import SSSPoseSwap

NODE_CLASS_MAPPINGS = {
    "SSSFaceBodyComposer": SSSFaceBodyComposer,
    "SSSClothingSwap": SSSClothingSwap,
    "SSSFaceSwap": SSSFaceSwap,
    "SSSHeadSwap": SSSHeadSwap,
    "SSSPoseSwap": SSSPoseSwap,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SSSFaceBodyComposer": "SSS Face/Body Composer",
    "SSSClothingSwap": "SSS Clothing Swap",
    "SSSFaceSwap": "SSS Face Swap",
    "SSSHeadSwap": "SSS Head Swap",
    "SSSPoseSwap": "SSS Pose Swap",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
