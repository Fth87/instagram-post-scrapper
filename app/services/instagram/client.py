from instagrapi import Client  # type: ignore
from app.config import INSTAGRAM_SESSIONID, RESIDENTIAL_PROXY_URL

class InstagramClientManager:
    """
    Handles Instagrapi client lifecycle, residential proxy routing,
    and browser SessionID authentication.
    """
    def __init__(self):
        self.client = Client()
        self._configure_proxy()

    def _configure_proxy(self):
        """Applies residential proxy routing before login if configured."""
        if RESIDENTIAL_PROXY_URL:
            try:
                self.client.set_proxy(RESIDENTIAL_PROXY_URL)
                print(f"[+] Residential proxy configured: {RESIDENTIAL_PROXY_URL}")
            except Exception as e:
                print(f"[-] Error setting residential proxy: {e}")

    def authenticate(self):
        """Authenticates with Instagram using the provided browser SessionID cookie."""
        if not INSTAGRAM_SESSIONID:
            raise ValueError(
                "INSTAGRAM_SESSIONID is not configured in your .env file. "
                "Please extract and paste the 'sessionid' cookie value from your active instagram.com session."
            )

        try:
            print("[*] Initiating direct authentication using browser SessionID cookie...")
            self.client.login_by_sessionid(INSTAGRAM_SESSIONID)
            print("[+] Authentication successful! Connected to Instagram.")
        except Exception as e:
            err_msg = str(e)
            raise RuntimeError(
                f"Failed to authenticate using browser SessionID: {err_msg}.\n"
                f"Hint: Ensure that the INSTAGRAM_SESSIONID value in your .env is correct "
                f"and that the cookie session has not expired in your browser."
            )
