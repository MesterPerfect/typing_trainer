import gettext
import builtins
import logging
from core.constants import BASE_DIR

logger = logging.getLogger(__name__)

def setup_translations(lang_code: str):
    """
    Initialize gettext translation and install the _() function globally.
    If the translation file is missing, it falls back to the original English strings.
    """
    locales_dir = BASE_DIR / "locales"
    
    # Use pathlib native method to create directory
    locales_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Load the translation domain 'messages' for the specified language
        lang_translations = gettext.translation(
            domain="messages", 
            localedir=str(locales_dir), 
            languages=[lang_code],
            fallback=True
        )
        
        # Install the _() function into Python's builtins globally
        lang_translations.install()
        logger.info(f"Localization loaded successfully for language: {lang_code}")
        
    except Exception as e:
        logger.warning(f"Failed to load localization for {lang_code}: {e}. Falling back to default strings.")
        # Ensure _() is still available as a fallback so the app doesn't crash
        builtins._ = lambda x: x
