from typing import Optional
from PIL import Image
from app.config import MEDIA_DIR

class MediaResolver:
    """
    Decoupled utility class managing media resolution and loading.
    """
    @staticmethod
    def load_local_image(image_url: str) -> Optional[Image.Image]:
        try:
            if "/media/" in image_url:
                relative_path = image_url.split("/media/")[-1]
                local_path = MEDIA_DIR / relative_path
                
                if local_path.exists():
                    return Image.open(local_path)
        except Exception as e:
            print(f"[-] Warning: Failed loading image file for multimodal lookup: {e}")
        return None
