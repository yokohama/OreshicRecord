from pathlib import Path

import ors.core
import ors.exec


def run(args):
    md_file = ors.core.md.prepare_file(args.command[0])
    prompt = ors.core.prompt.build()
    cmd = Path(args.command[0]).name.lower()
    use_pty = cmd in ors.core.settings.get_auto_interactive()

    with open(md_file, "a", encoding="utf-8") as fp:
        ors.core.md.write_header(fp, args.message, prompt, args.command)
        try:
            if use_pty:
                ors.exec.pty.run(args.command, fp, args.quiet)
            else:
                ors.exec.stream.run(
                    args.command,
                    fp,
                    args.quiet
                )
        finally:
            ors.core.md.close_output(fp)
