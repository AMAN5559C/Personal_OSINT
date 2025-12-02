import time
from playwright.sync_api import sync_playwright

def scrape_images_from_url(page, url):
    """
    Visits a single URL, scrolls to load content, and extracts all unique image URLs.
    Improved to look for 'src', 'data-src', and 'srcset'.
    """
    print(f"--- Visiting: {url} ---")
    try:
        # Go to the URL and wait for network to be idle (better for full load)
        page.goto(url, timeout=60000, wait_until="networkidle")
        
        # --- SCROLLING LOGIC ---
        # Scroll down a few times to trigger lazy-loading images.
        for i in range(1, 4): 
            print(f"Scrolling page... ({i}/3)")
            page.mouse.wheel(0, 5000) 
            time.sleep(2) # Wait for data to load after scroll

        # Find all <img> tags
        img_elements = page.locator("img").all()
        img_urls = set()

        for img in img_elements:
            try:
                # Check common attributes for image URLs
                possible_urls = [
                    img.get_attribute("src"),
                    img.get_attribute("data-src"),
                    img.get_attribute("srcset") 
                ]
                
                for src in possible_urls:
                    if src:
                        # Handle srcset: take the first URL if it's a list
                        if " " in src:
                             src = src.split(" ")[0]
                        # Handle protocol-relative URLs (common on Wikipedia)
                        if src.startswith("//"):
                            src = "https:" + src
                        
                        if src.startswith("http"):
                            img_urls.add(src)
            except:
                continue # If one image fails, just keep going

        print(f"Found {len(img_urls)} unique images on {url}")
        return list(img_urls)

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

def run_batch_scrape(url_list):
    """
    Main entry point for batch scraping.
    Accepts a list of target URLs.
    Returns a dictionary where keys are URLs and values are lists of image links found there.
    """
    results = {}

    print("Starting Playwright Engine...")
    with sync_playwright() as p:
        # Launch invisible browser (headless=True)
        browser = p.chromium.launch(headless=True)
        
        # Create a new browser context with a standard user agent
        context = browser.new_context(
             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for target_url in url_list:
            if not target_url.strip():
                continue # Skip empty lines
                
            found_images = scrape_images_from_url(page, target_url)
            results[target_url] = found_images
            
            # Polite wait between different sites
            time.sleep(2) 

        browser.close()
    
    print("Batch scrape finished.")
    return results

# --- TEMPORARY TESTING BLOCK ---
if __name__ == "__main__":
    # Test with Wikipedia
    test_urls = [
        "https://en.wikipedia.org/wiki/Kallen_Stadtfeld"
    ]
    scraped_data = run_batch_scrape(test_urls)
    
    # Print results to verify
    for url, images in scraped_data.items():
        print(f"\nResults for {url}:")
        for img in images[:5]: # Print first 5 images found
            print(f" - {img}")