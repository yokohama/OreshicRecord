import sys

import ors.core
import ors.features
import ors.core
import ors.exec


def run(args):
    if len(args.search) == 1:
        ors.features.common.list_files_ascii("track")
        return

    if len(args.search) == 2:
        ors.features.common.search_file_ascii_by_id("track", args.search[1])
        return

    if len(args.search) == 3:
        file_id, entry_id = args.search[1], args.search[2]

        if args.run and args.delete:
            print(
                "[ors] cannot use --run and --del together",
                file=sys.stderr
            )
            sys.exit(2)

        if args.run:
            ors.features.common.run_entry_by_ids(
                "track",
                file_id, entry_id,
                args.message,
                args.quiet
            )
            return

        if args.delete:
            ors.features.common.delete_entry_by_ids(
                "track",
                file_id,
                entry_id
            )
            return

        ors.features.common.show_entry_detail_by_ids(
            "track",
            file_id,
            entry_id
        )
        return

    print(
        "[ors] usage: -s track [file_id [entry_id]] [--run|--del]",
        file=sys.stderr
    )
