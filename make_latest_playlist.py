import playlist_tools as pt
import datetime

if __name__ == "__main__":
    print("Creating playlist on Spotify of the 6+ out of 10 Metal album reviews over the last 2 weeks from metal-temple.com...")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=14)).strftime("%Y-%m-%d")

    pt.create_metal_album_list(start_date, end_date, 6)
    pt.create_playlist(f'albumlist_metal-temple_{start_date}_{end_date}.json', 3)

    print("Latest playlist created successfully! Check Spotify and enjoy!")