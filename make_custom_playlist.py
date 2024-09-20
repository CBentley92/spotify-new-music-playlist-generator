import playlist_tools as pt
from datetime import datetime
import os
import argparse

if __name__ == "__main__":
    # Initialize argparse
    parser = argparse.ArgumentParser(description="Create a Spotify playlist from reviewed tracks.")

    # Add arguments
    parser.add_argument('-sd', '--start-date', type=str, required=True, help="Start date in the format YYYY-MM-DD")
    parser.add_argument('-ed', '--end-date', type=str, required=True, help="End date in the format YYYY-MM-DD")
    parser.add_argument('-ms', '--min-score', type=int, default=6, help="Minimum review score out of 10 (default: 6)")
    parser.add_argument('-ro', '--randomise-order', type=bool, default=False, help="Randomise the order of the tracks in the playlist (default: False)")
    parser.add_argument('-ns', '--songs-per-album', type=int, default=2, help="Number of songs per album to include in playlist (default: 2)")
    parser.add_argument('-od', '--output-dir', type=str, default='.', help="Directory to save the review list (default: current directory)")

    # Parse the arguments
    args = parser.parse_args()

    # Validate and parse the dates
    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError:
        print("Error: Dates must be in the format YYYY-MM-DD")
        exit(1)

    # Ensure the output directory exists
    if not os.path.exists(args.output_dir):
        print(f"Error: Output directory {args.output_dir} does not exist.")
        exit(1)

    # Fetch the track list using the provided arguments
    pt.create_metal_album_list(args.start_date, args.end_date, args.min_score, args.output_dir)

    # Create the Spotify playlist
    pt.create_playlist(f'albumlist_metal-temple_{args.start_date}_{args.end_date}.json', randomise_order=args.randomise_order, songs_per_album=args.songs_per_album)

