from .feedly2instapaper import main
import argparse


def _cli():
    # Command line parsing
    parser = argparse.ArgumentParser(
        prog="feedl2instapaper",
    )
    parser.add_argument(
        "-e",
        "--env",
        help="Path to .env file",
        default=".env",
    )
    parser.add_argument(
        "-a",
        "--archive",
        help="Archive pages",
        action="store_true",
    )
    main(env_file=parser.parse_args().env, archive=parser.parse_args().archive)


if __name__ == "__main__":
    _cli()
