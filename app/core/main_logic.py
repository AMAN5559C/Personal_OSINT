# app/core/main_logic.py
from app.core.scraper import run_batch_scrape
from app.core.face_matcher import load_target_face, check_match
import time

def run_full_scan(target_image_path, url_list, progress_callback=None):
    """
    The master function that orchestrates the whole process.
    """
    print(f"--- STARTING SCAN ---")
    
    # 1. Load Target Face
    target_encoding = load_target_face(target_image_path)
    if target_encoding is None:
        return {"error": "Could not find a face in the uploaded target image."}

    # 2. Run Batch Scraper
    if progress_callback: progress_callback("Phase 1: Scraping target sites...")
    print("Phase 1: Scraping URLs...")
    scraped_data = run_batch_scrape(url_list)
    
    total_images = sum(len(imgs) for imgs in scraped_data.values())
    print(f"Scraping complete. Found {total_images} total images to analyze.")

    # 3. Compare Faces
    if progress_callback: progress_callback(f"Phase 2: Analyzing {total_images} images...")
    print("Phase 2: Starting face analysis...")
    
    final_matches = []
    count = 0
    for source_url, image_links in scraped_data.items():
        for img_link in image_links:
            count += 1
            # Optional: print progress every 10 images so we know it's not frozen
            if count % 10 == 0:
                print(f"Analyzed {count}/{total_images} images...")

            is_match, confidence = check_match(target_encoding, img_link)
            if is_match:
                match_data = {
                    "source_site": source_url,
                    "image_url": img_link,
                    "confidence": round(confidence, 2),
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                final_matches.append(match_data)

    # 4. Final Report Data
    print(f"--- SCAN FINISHED. Found {len(final_matches)} matches. ---")
    return {
        "status": "success",
        "total_scanned": total_images,
        "matches": final_matches
    }