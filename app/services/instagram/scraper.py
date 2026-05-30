import time
import random
from instagrapi.exceptions import (  # type: ignore
    ClientError,
    FeedbackRequired,
    PleaseWaitFewMinutes,
    RateLimitError
)
from app.config import MEDIA_DIR
from app.services.instagram.client import InstagramClientManager
from app.services.instagram.exceptions import InstagramRateLimitException

class InstagramScraperService:
    """
    Handles fetching user profile, listing media posts,
    applying jitter delays, and downloading cover photos locally.
    """
    def __init__(self, client_manager: InstagramClientManager):
        self.client_manager = client_manager

    def _jitter(self):
        """Inject randomized delay between 5.0 to 15.0 seconds to mimic human interaction."""
        delay = random.uniform(5.0, 15.0)
        print(f"[Jitter] Sleeping for {delay:.2f} seconds to avoid anti-bot detection...")
        time.sleep(delay)

    def scrape_latest_posts_sync(self, username: str, limit: int, base_url: str) -> list[dict]:
        """
        Scrapes the latest posts from a public Instagram profile.
        Enforces human jitter and downloads cover photos locally.
        """
        # Ensure client is authenticated
        self.client_manager.authenticate()
        client = self.client_manager.client

        try:
            # 1. Resolve username to target user ID
            print(f"[*] Resolving user ID for @{username}...")
            user_id = client.user_id_from_username(username)
            print(f"[+] User ID resolved: {user_id}")
            
            # Inject jitter after API call
            self._jitter()

            # 2. Fetch latest media posts
            print(f"[*] Fetching N={limit} latest media posts...")
            medias = client.user_medias(user_id, amount=limit)
            print(f"[+] Successfully fetched {len(medias)} posts.")
            
            # Inject jitter after fetching media
            self._jitter()

        except PleaseWaitFewMinutes as pwe:
            raise InstagramRateLimitException(f"Instagram asked to wait: {pwe}")
        except FeedbackRequired as fe:
            raise InstagramRateLimitException(
                f"Instagram action blocked (Feedback Required). Proxy or account may be flagged: {fe}"
            )
        except RateLimitError as rle:
            raise InstagramRateLimitException(f"Instagram API rate limit exceeded: {rle}")
        except ClientError as ce:
            raise RuntimeError(f"Instagrapi Client Error: {ce}")
        except Exception as e:
            raise RuntimeError(f"Error fetching profile/media: {e}")

        # Directory where downloaded files are saved
        user_media_dir = MEDIA_DIR / username
        user_media_dir.mkdir(parents=True, exist_ok=True)

        scraped_posts = []

        for media in medias:
            # Only process photos (Type 1) or carousel albums (Type 8)
            if media.media_type not in (1, 8):
                print(f"[*] Skipping non-photo media code: {media.code} (Type: {media.media_type})")
                continue

            local_filepath = user_media_dir / f"{media.code}.jpg"

            # Download the picture if not already cached locally
            if not local_filepath.exists():
                try:
                    print(f"[*] Downloading post cover image: {media.code}...")
                    temp_path = client.photo_download(
                        media_pk=media.pk,
                        folder=user_media_dir
                    )
                    
                    # Rename the downloaded file to exactly code.jpg to stay consistent
                    if temp_path.exists() and temp_path != local_filepath:
                        if local_filepath.exists():
                            local_filepath.unlink()
                        temp_path.rename(local_filepath)
                        
                    print(f"[+] Downloaded and stored image as: {local_filepath.name}")
                    
                    # Jitter Delay after downloading
                    self._jitter()

                except Exception as e:
                    print(f"[-] Warning: Failed to download cover image for media {media.code}: {e}")

            # Construct static persistent local URL
            image_url = f"{base_url}media/{username}/{media.code}.jpg"

            scraped_posts.append({
                "shortcode": media.code,
                "caption": media.caption_text if media.caption_text else None,
                "image_url": image_url,
                "timestamp": media.taken_at,
                "likes": media.like_count,
                "comments_count": media.comment_count
            })

        return scraped_posts
