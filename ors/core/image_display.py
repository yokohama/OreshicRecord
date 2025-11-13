"""画像表示のためのユーティリティ関数"""
import sys
import re
import os
from pathlib import Path


def convert_image_paths(content: str, md_file_path: Path) -> str:
    current_dir = Path.cwd()
    md_dir = md_file_path.parent

    # 画像パスのパターン（markdown記法）
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    def replace_path(match):
        alt_text = match.group(1)
        original_path = match.group(2)

        # 絶対パスやHTTPで始まるものはそのまま
        if (Path(original_path).is_absolute() or
                original_path.startswith(('http://', 'https://'))):
            return match.group(0)

        # ./md_images/ で始まる相対パスを変換
        if original_path.startswith('./md_images/'):
            # MDファイルの場所を基点とした絶対パス
            absolute_image_path = (
                md_dir / original_path.lstrip('./')
            ).resolve()

            # 現在のディレクトリからの相対パス
            try:
                relative_from_current = os.path.relpath(
                    absolute_image_path, current_dir
                )
                return f'![{alt_text}]({relative_from_current})'
            except (ValueError, OSError):
                # 相対パスにできない場合は絶対パスを使用
                return f'![{alt_text}]({absolute_image_path})'

        # その他のパスはそのまま
        return match.group(0)

    return re.sub(image_pattern, replace_path, content)


def display_content_with_images(content: str, md_file_path: Path):
    # 画像パスを変換してから出力
    converted_content = convert_image_paths(content, md_file_path)
    sys.stdout.write(converted_content)
