"""
CLI command for Daily Learning Server.
"""
import argparse
import logging
import sys
from pathlib import Path

from ..core.daily_learning_server import DailyLearningServer

logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Start the Daily Learning Report Server")
    parser.add_argument(
        "--dev-mode",
        action="store_true",
        default=True,  # Default to dev mode for development
        help="Trigger report in 3 seconds for testing (default: True)",
    )
    parser.add_argument(
        "--no-dev-mode",
        action="store_false",
        dest="dev_mode",
        help="Disable dev mode (use production schedule)",
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Optional status port (unused currently, reserved for future health checks)",
    )
    parser.add_argument(
        "--trigger-hour",
        type=int,
        default=21,
        help="Hour to trigger report in production mode (0-23, default: 21 for 9 PM)",
    )
    parser.add_argument(
        "--project-path",
        type=str,
        default=".",
        help="Path to project root (default: current directory)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )

    args = parser.parse_args()

    # Set logging level
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Resolve project path
    project_path = Path(args.project_path).resolve()
    if not project_path.exists():
        logger.error(f"Project path does not exist: {project_path}")
        sys.exit(1)

    # Create and start server
    server = DailyLearningServer(
        project_path=project_path,
        dev_mode=args.dev_mode,
        trigger_hour=args.trigger_hour,
    )

    try:
        server.start()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
