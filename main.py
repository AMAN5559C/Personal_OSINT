import asyncio
import sys

# FIX FOR WINDOWS PLAYWRIGHT ERROR
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
# END FIX

import streamlit as st
import os
import tempfile
import time
from app.core.main_logic import run_full_scan
from app.core.report_gen import create_pdf_report 

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Kallen Sentinel - Professional",
    page_icon="/osint_icon.ico",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    [data-testid="stHeader"] { display: none; }
    .block-container { padding-top: 1rem; }
    div.stButton > button { width: 100%; border-radius: 5px; height: 3em; }
    textarea { font-family: monospace; }
    /* Make right panel scrollable if results get long */
    [data-testid="column"]:nth-of-type(3) {
        max-height: 90vh;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("Kallen Sentinel __ Professional")
st.markdown("---")

# --- MAIN LAYOUT ---
left_panel, center_panel, right_panel = st.columns([1, 2, 1])

# --- LEFT PANEL (CONTROLS) ---
with left_panel:
    st.subheader("Control Panel")
    with st.expander("1. Target Acquisition", expanded=True):
        uploaded_file = st.file_uploader("Select Target Image", type=['jpg', 'png', 'jpeg'])
        
    with st.expander("2. Intelligence Sources", expanded=True):
        url_input = st.text_area("Target URLs (One per line)", height=250, placeholder="https://...")
    
    st.write("")
    start_btn = st.button("▶ INITIATE SCAN", type="primary")

# --- CENTER PANEL (PERSISTENT PREVIEW) ---
with center_panel:
    st.subheader("Target Preview")
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True, caption="Locked Target")
    else:
        st.info("Awaiting target image upload...")

# --- RIGHT PANEL (LOGS & RESULTS PLACEHOLDER) ---
with right_panel:
    st.subheader("System Logs")
    log_area = st.empty()
    
    # Placeholder for results to appear LATER, below logs
    results_container = st.container()

# --- EXECUTION ---
if start_btn:
    if not uploaded_file or not url_input.strip():
        left_panel.error("❌ ERROR: Missing Input")
    else:
        # Setup
        target_urls = [url.strip() for url in url_input.split('\n') if url.strip()]
        current_logs = ["System Ready."]
        
        def update_logs(msg):
            current_logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
            # Keep last 10 lines to save space in right panel now that results are there too
            log_area.code("\n".join(current_logs[-10:]), language="bash")

        update_logs("Initiating scan sequence...")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            # Run Scan (with spinner in center to show activity)
            with center_panel:
                with st.spinner("Scanning target vectors..."):
                    results = run_full_scan(tmp_path, target_urls, progress_callback=update_logs)

            update_logs("--- SCAN COMPLETE ---")
            
            # --- POPULATE RIGHT PANEL RESULTS ---
            with results_container:
                st.markdown("---")
                st.subheader("🎯 Scan Results")
                
                # 1. Download Button
                pdf_path = create_pdf_report(tmp_path, results['matches'])
                with open(pdf_path, "rb") as f:
                     st.download_button("📄 DOWNLOAD PDF", f.read(), file_name="report.pdf", mime="application/pdf", type="primary", use_container_width=True)

                # 2. Summary
                if results['matches']:
                    st.success(f"Found {len(results['matches'])} matches.")
                    # 3. Match List
                    for i, match in enumerate(results['matches'], 1):
                        with st.expander(f"#{i} - {match['confidence']}% Match"):
                             # Smaller images in right panel to fit better
                             st.image(match['image_url'], use_container_width=True)
                             st.caption(f"Source: {match['source_site']}")
                else:
                    st.warning("No matches found.")

        except Exception as e:
            left_panel.error(f"ERROR: {e}")
            update_logs(f"FAILURE: {e}")
        finally:
            if os.path.exists(tmp_path): os.remove(tmp_path)