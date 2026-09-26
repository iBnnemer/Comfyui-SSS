from .composer_node import AAFaceBodyComposer
from .clothing_swap_node import AAClothingSwap
from .face_swap_node import AAFaceSwap
from .head_swap_node import AAHeadSwap
from .pose_swap_node import AAPoseSwap

NODE_CLASS_MAPPINGS = {
    "AAFaceBodyComposer": AAFaceBodyComposer,
    "AAClothingSwap": AAClothingSwap,
    "AAFaceSwap": AAFaceSwap,
    "AAHeadSwap": AAHeadSwap,
    "AAPoseSwap": AAPoseSwap,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "AAFaceBodyComposer": "AA Face/Body Composer",
    "AAClothingSwap": "AA Clothing Swap",
    "AAFaceSwap": "AA Face Swap",
    "AAHeadSwap": "AA Head Swap",
    "AAPoseSwap": "AA Pose Swap",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
