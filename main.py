from utils.cli import parse_arguments
from utils.logger import setup_logger
from app.application import run_app

if __name__ == "__main__":
    # 1. Parse CLI arguments first
    args = parse_arguments()
    
    # 2. Setup logger with CLI overrides
    setup_logger(cli_level=args.log_level, no_log_time=args.no_log_time)
    
    # 3. Launch the application passing the arguments
    run_app(args)
