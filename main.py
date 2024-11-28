import streamlit as st
from scrape import (scrape_website, extract_body_content, clean_body_content, split_dom_content)
# from parse_ollama import parse_with_ollama
from parse_azureai import parse_with_azureai

st.title("AI WebScraper") # display a title
url = st.text_input("Enter a website URL: ") # display a text input box

if st.button("Scrape site"): # if the user clicks the "Scrape site" button
    st.write("Scraping website...") # display a message
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_body_content = clean_body_content(body_content)
    st.session_state.dom_content = cleaned_body_content
    with st.expander("View DOM content"): # display a collapsible section
        st.text_area(label="DOM content", value=cleaned_body_content, height=300) # display the DOM content

if "dom_content" in st.session_state: # if the DOM content is in the session state
    parse_description = st.text_area("Describe what you want to parse?")
    if st.button("Parse Content"):
        st.write("Parsing content...")
        dom_chunks = split_dom_content(st.session_state.dom_content)
        # result = parse_with_ollama(dom_chunks, parse_description)
        result = parse_with_azureai(dom_chunks, parse_description)
        st.write(result)