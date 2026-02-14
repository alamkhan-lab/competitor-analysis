import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(layout="wide")
st.title("🕵️‍♂️ Competitor Header Spy")
st.write("Compare the content structure of your competitors side-by-side.")

# 1. Input: Multiple URLs
urls_input = st.text_area("Paste URLs (one per line):", placeholder="https://example.com/page1\nhttps://example.com/page2")

if st.button("Analyze Now"):
    urls = urls_input.split('\n')
    all_data = []

    for url in urls:
        url = url.strip()
        if url:
            try:
                res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # Find all headers
                headers = soup.find_all(['h1', 'h2', 'h3'])
                header_list = [f"{h.name.upper()}: {h.text.strip()}" for h in headers]
                
                all_data.append({"URL": url, "Headers": "\n".join(header_list)})
            except Exception as e:
                st.error(f"Error crawling {url}: {e}")

    # 2. Display: Side-by-Side Columns
    if all_data:
        cols = st.columns(len(all_data))
        for i, data in enumerate(all_data):
            with cols[i]:
                st.info(f"**URL:** {data['URL']}")
                # Using a text area so it's easy to copy
                st.text_area("Structure:", data['Headers'], height=400)