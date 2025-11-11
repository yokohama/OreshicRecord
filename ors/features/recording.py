from pathlib import Path

import ors.core
import ors.md
import ors.exec


def bar(args):
    md_file = ors.md.writer.prepare_md_file(args.command[0])
    prompt = ors.core.prompt.build_prompt()
    cmd = Path(args.command[0]).name.lower()
    use_pty = cmd in ors.core.settings.get_auto_interactive()

    with open(md_file, "a", encoding="utf-8") as fp:
        ors.md.writer.md_header(fp, args.message, prompt, args.command)
        try:
            if use_pty:
                ors.exec.pty_runner.run_via_pty(args.command, fp, args.quiet)
            else:
                ors.exec.stream_runner.run_stream_tee(
                    args.command,
                    fp,
                    args.quiet
                )
        finally:
            ors.md.writer.md_close_output(fp)
