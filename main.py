import subprocess
from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def convert_videos(
    dav_videos_path: Path = typer.Argument(
        ..., exists=True, help="Path of input .dav videos"
    ),
    mp4_videos_path: Path = typer.Argument(
        ..., exists=True, help="Path of output .mp4 videos"
    ),
    output_video_height: int = typer.Argument(
        576,
        min=100,
        clamp=True,
        help="Height (pixels) of output videos",
    ),
    output_video_width: int = typer.Argument(
        704,
        min=100,
        clamp=True,
        help="Width (pixels) of output videos",
    ),
    rename_videos: bool = typer.Option(
        False,
        "--rename",
        "-r",
        help="Rename output videos name (base on parent folder name) or not.",
    ),
):
    if rename_videos:
        # TODO: replace dav_videos_path.glob("*") with regex
        for camera_folder_path in dav_videos_path.glob("*"):
            camera_name = camera_folder_path.stem
            for dav_video_path in camera_folder_path.glob("**/*.dav"):
                video_name = dav_video_path.stem[13:]
                subprocess.call(
                    [
                        "ffmpeg",
                        "-y",
                        "-i",
                        dav_video_path,
                        "-vf",
                        f"scale={output_video_width}:{output_video_height}",
                        "-vcodec",
                        "h264",
                        mp4_videos_path / f"{camera_name}_{video_name}.mp4",
                        "-loglevel",
                        "error",
                    ]
                )
    else:
        for dav_video_path in dav_videos_path.glob("**/*.dav"):
            video_name = dav_video_path.stem
            subprocess.call(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    dav_video_path,
                    "-vf",
                    f"scale={output_video_width}:{output_video_height}",
                    "-vcodec",
                    "h264",
                    mp4_videos_path / f"{video_name}.mp4",
                    "-loglevel",
                    "error",
                ]
            )


if __name__ == "__main__":
    app()
