import sys
import argparse


# ==========================================================
# 引数パース
# ==========================================================


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="org",
        description="Execute a command and save its output to Markdown."
    )
    parser.add_argument(
        "-s", "--search",
        nargs="+",
        metavar="SEARCH",
        help="search mode: -s (command|track|writeup|query) [id ...]"
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="with -s (command|track) <file_id> <entry_id> -> "
             "re-run that entry now and record"
    )
    parser.add_argument(
        "--del",
        dest="delete",
        action="store_true",
        help="with -s (command|track) <file_id> <entry_id> -> "
             "delete that entry (if Count becomes 0, remove file)"
    )
    parser.add_argument(
        "-m", "--message",
        metavar="MESSAGE",
        help="optional note to save"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="do not save output to file"
    )
    parser.add_argument(
        "-t", "--track",
        metavar="NAME",
        help="(this run only) set ORESHIC_TRACK for this process"
    )
    parser.add_argument(
        "-u", "--unset",
        action="store_true",
        help="(this run only) unset ORESHIC_TRACK for this process"
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="command to execute"
    )
    return parser


def parse_args(argv):
    parser = build_parser()
    try:
        return parser.parse_args(argv)
    except SystemExit:
        print("\n[ors] invalid or conflicting arguments.\n")
        parser.print_help()
        sys.exit(2)


def print_help():
    build_parser().print_help()
