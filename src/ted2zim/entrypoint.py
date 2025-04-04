import argparse

from ted2zim.constants import ALL, MATCHING, NAME, NONE, SCRAPER, get_logger, set_debug


def main():
    parser = argparse.ArgumentParser(
        prog=NAME,
        description="Scraper to create ZIM files from TED talks topics or playlists",
    )
    # Create a mutually exclusive group for content source
    source_group = parser.add_mutually_exclusive_group(required=True)

    source_group.add_argument(
        "--links",
        help="Comma-separated TED talk URLs to scrape, each in the format: https://www.ted.com/talks/<talk_slug>",
    )

    source_group.add_argument(
        "--topics",
        help="Comma-separated list of topics to scrape; as given on ted.com/talks",
    )

    source_group.add_argument(
        "--playlist",
        help="A playlist ID from ted.com/playlists to scrape videos from",
    )

    parser.add_argument(
        "--languages", help="Comma-separated list of languages to filter videos"
    )

    parser.add_argument(
        "--locale",
        help="The locale to use in the UI (can be iso language code / locale)",
        dest="locale_name",
        default="eng",
    )

    parser.add_argument(
        "--subtitles-enough",
        help="Whether to include videos that have a subtitle in requested --languages "
        "if audio is in another language",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--subtitles",
        help=f"Language setting for subtitles. {ALL}: include all available subtitles, "
        f"{MATCHING} (default): only subtitles matching --languages, {NONE}: include no"
        " subtitle. Also accepts comma-separated list of language codes",
        default=MATCHING,
        dest="subtitles_setting",
    )

    parser.add_argument(
        "--format",
        help="Format to download/transcode video to. webm is smaller",
        choices=["mp4", "webm"],
        default="webm",
        dest="video_format",
    )

    parser.add_argument(
        "--low-quality",
        help="Re-encode video using stronger compression",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--autoplay",
        help="Enable autoplay on video articles. Behavior differs on "
        "platforms/browsers.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--name",
        help="ZIM name. Used as identifier and filename (date will be appended)",
        required=True,
    )

    parser.add_argument(
        "--title",
        help="Custom title for your ZIM. Based on selection otherwise.",
    )

    parser.add_argument(
        "--description",
        help="Custom description for your ZIM. Based on selection otherwise.",
    )

    parser.add_argument(
        "--long-description",
        help="Custom long description for your ZIM.",
    )

    parser.add_argument("--creator", help="Name of content creator", default="TED")

    parser.add_argument(
        "--publisher", help="Custom publisher name (ZIM metadata)", default="openZIM"
    )

    parser.add_argument(
        "--tags",
        help="List of comma-separated Tags for the ZIM file. category:ted, ted, and "
        "_videos:yes added automatically",
    )

    parser.add_argument(
        "--optimization-cache",
        help="URL with credentials and bucket name to S3 Optimization Cache",
        dest="s3_url_with_credentials",
    )

    parser.add_argument(
        "--use-any-optimized-version",
        help="Use files on S3 cache if present, whatever the version",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--output",
        help="Output folder for ZIM file",
        default="/output",
        dest="output_dir",
    )

    parser.add_argument(
        "--tmp-dir",
        help="Path to create temp folder in. Used for building ZIM file. Receives all "
        "data (storage space)",
    )

    parser.add_argument(
        "--zim-file",
        help="ZIM file name (based on --name if not provided)",
        dest="fname",
    )

    parser.add_argument(
        "--no-zim",
        help="Don't produce a ZIM file, create build folder only.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--keep",
        help="Don't remove build folder on start (for debug/devel)",
        default=False,
        action="store_true",
        dest="keep_build_dir",
    )

    parser.add_argument(
        "--debug", help="Enable verbose output", action="store_true", default=False
    )

    parser.add_argument(
        "--threads",
        help="Maximum number of parallel threads to use",
        default=1,
        type=int,
    )

    parser.add_argument(
        "--version",
        help="Display scraper version and exit",
        action="version",
        version=SCRAPER,
    )

    parser.add_argument(
        "--disable-metadata-checks",
        help="Disable validity checks of metadata according to openZIM conventions",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--language-threshold",
        help="Consider languages present in at least percentage of videos",
        default=0.5,
        type=float,
    )

    args = parser.parse_args()
    set_debug(args.debug)
    logger = get_logger()

    from ted2zim.scraper import Ted2Zim

    try:
        if not args.subtitles_setting:
            parser.error("--subtitles cannot take an empty string")

        if not args.threads >= 1:
            parser.error("--threads must be provided a positive integer")

        if not 0 < args.language_threshold <= 1:
            parser.error("--language-threshold must be between 0 and 1.")

        scraper = Ted2Zim(**dict(args._get_kwargs()))
        scraper.run()
    except Exception as exc:
        logger.error(f"FAILED. An error occurred: {exc}")
        if args.debug:
            logger.exception(exc)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
