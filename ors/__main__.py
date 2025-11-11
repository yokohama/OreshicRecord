import sys

import ors.cli
import ors.features


def main():
    # 引数ゼロならヘルプだけ表示して終了
    if len(sys.argv) == 1:
        ors.cli.parser.print_help()
        return 0

    args = ors.cli.parser.parse_args(sys.argv[1:])

    # このプロセス内だけトラック名を設定/解除（親シェルには影響しない）
    #if args.track:
    #    os.environ["ORESHIC_TRACK"] = args.track
    #    print(f("[ors] track set (process): {args.track}"))
    #    if not args.command and not args.search and not args.unset:
    #        return

    #if args.unset:
    #    os.environ.pop("ORESHIC_TRACK", None)
    #    print("[ors] track unset (process)")
    #    if not args.command and not args.search:
    #        return

    # search mode
    if args.search:
        mode = args.search[0].lower()

        if mode == "command":
            ors.features.command.hoge(args)
            sys.exit(2)

        elif mode == "track":
            ors.features.track.moge(args)
            sys.exit(2)

        elif mode == "writeup":
            ors.features.writeup.fuga(args)
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
    ors.features.recording.bar(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
