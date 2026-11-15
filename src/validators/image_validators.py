"""
Image validation and preprocessing utilities for facial recognition.
"""

from typing import Tuple, Optional
from PIL import Image
import numpy as np
from src.config.app_config import MAX_IMAGE_DIMENSION

def validate_and_prepare_image(image: Optional[Image.Image]) -> Tuple[bool, str, Optional[np.ndarray]]:
    """
    Validates a PIL Image, ensures proper RGB format, and scales down oversized
    images to prevent out-of-memory or high latency during face detection.
    Returns: (is_valid, error_message, numpy_rgb_array)
    """
    if image is None:
        return False, "No image provided.", None

    try:
        # Convert image to RGB format (handles RGBA, Palette, Grayscale)
        rgb_image = image.convert("RGB")
        width, height = rgb_image.size

        if width < 20 or height < 20:
            return False, "Image resolution is too low to detect facial features.", None

        # Scale down if either dimension exceeds MAX_IMAGE_DIMENSION
        if max(width, height) > MAX_IMAGE_DIMENSION:
            scale = MAX_IMAGE_DIMENSION / float(max(width, height))
            new_size = (int(width * scale), int(height * scale))
            rgb_image = rgb_image.resize(new_size, Image.Resampling.LANCZOS)

        np_array = np.array(rgb_image)
        return True, "", np_array

    except Exception as e:
        return False, f"Failed to process image: {str(e)}", None
