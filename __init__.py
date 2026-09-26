from .composer_node import SSSFaceBodyComposer
from .clothing_swap_node import SSSClothingSwap
from .face_swap_node import SSSFaceSwap
from .head_swap_node import SSSHeadSwap

NODE_CLASS_MAPPINGS = {
    "SSSFaceBodyComposer": SSSFaceBodyComposer,
    "SSSClothingSwap": SSSClothingSwap,
    "SSSFaceSwap": SSSFaceSwap,
    "SSSHeadSwap": SSSHeadSwap,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SSSFaceBodyComposer": "SSS Face/Body Composer",
    "SSSClothingSwap": "SSS Clothing Swap",
    "SSSFaceSwap": "SSS Face Swap",
    "SSSHeadSwap": "SSS Head Swap",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
