import m3u8_To_MP4

if __name__ == '__main__':
    # 1. Download videos from uri.
    m3u8_To_MP4.multithread_download('https://stream-private-ht.project1content.com/hls/48a/6a0/07f/c98/461/b9d/3a0/de6/302/fc5/59/video/scene,_320p,_480p,_720p,_1080p,_2160p,.mp4.urlset/master.m3u8?validto=1696713230&ip=49.43.34.160&hash=UXwVAW0G2jIe7cGTjnmp%2FqvIpZo%3D',mp4_file_dir='videos2',mp4_file_name='Test1')

    # # 2. Download videos from existing m3u8 files.
    # m3u8_To_MP4.multithread_file_download('http://videoserver.com/playlist.m3u8',m3u8_file_path)

    # For compatibility, i reserve this api, but i do not recommend to you again.
    # m3u8_To_MP4.download('http://videoserver.com/playlist.m3u8')