
from utils.logger import setup_logger

if __name__ == "__main__":
    # Initialize logger BEFORE importing application modules
    # to ensure all module-level operations are captured.
    setup_logger()
    
    from app.application import run_app
    run_app()
