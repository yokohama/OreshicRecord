import sys
from pathlib import Path

import ors.cli
import ors.features


def main():
    # 引数ゼロならヘルプだけ表示して終了
    if len(sys.argv) == 1:
        ors.cli.parser.print_help()
        return 0

    args = ors.cli.parser.parse_args(sys.argv[1:])

    #print(args)
    #return 0

    if args.track:
        with open(
            ors.core.settings.get_track_name_file(),
            "w",
            encoding="utf-8"
        ) as f:
            f.write(args.track)

        print(f"[ors] track set (process): {args.track}")

        if not args.command and not args.search and not args.unset:
            return

    if args.unset:
        path = Path(ors.core.settings.get_track_name_file())
        if path.exists():
            path.unlink()

        print("[ors] track unset (process)")

        if not args.command and not args.search:
            return

    # search mode
    if args.search:
        mode = args.search[0].lower()

        if mode == "command":
            ors.features.command.run(args)
            sys.exit(2)

        elif mode == "track":
            ors.features.track.run(args)
            sys.exit(2)

        elif mode == "writeup":
            ors.features.writeup.run(args)
            sys.exit(2)

        else:
            print(
                "[ors] usage: -s (command|track|writeup) [id ...]",
                file=sys.stderr
            )
            sys.exit(2)

    # execute mode
    if not args.command:
        print("Missing command", file=sys.stderr)
        sys.exit(2)

    # recording mode
    ors.features.recording.run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
