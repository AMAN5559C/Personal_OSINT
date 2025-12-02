# test_matcher.py
from app.core.face_matcher import load_target_face, check_match

# 1. Load the local target
target_encoding = load_target_face("test_target.jpg")

if target_encoding is not None:
    # 2. URL of the OTHER photo of the same person
    test_url = "https://imgs.search.brave.com/1nL-YoBPHi2r_qI_vsCMWvDTXC0202L4kn_wWKT2F5o/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTQ4/NjkyNzYzNi9waG90/by9uZXcteW9yay1u/ZXcteW9yay1qZW5u/YS1vcnRlZ2EtYXR0/ZW5kcy10aGUtMjAy/My1tZXQtZ2FsYS1j/ZWxlYnJhdGluZy1r/YXJsLWxhZ2VyZmVs/ZC1hLWxpbmUtb2Yu/anBnP3M9NjEyeDYx/MiZ3PTAmaz0yMCZj/PUFYWlF3d1J0Zm55/M1M4NG9sNXJKY3FD/WGY1Qzl1YVFGb0VY/TDJjd095c2s9" 
    
    print(f"Testing match against: {test_url}")
    is_match, conf = check_match(target_encoding, test_url)
    
    if is_match:
        print("SUCCESS: The matcher recognized the person!")
    else:
        print("FAILURE: Did not recognize the person (or couldn't download URL).")