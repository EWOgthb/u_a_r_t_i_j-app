import streamlit as st
import json
from io import StringIO
search_text = "e844387f-ab63-4fd5-b601-b8d71c1bc561"
replace_with = "088ad712-70ef-46ee-9d86-734dd1606ee7"

st.info(f"Will replace all occurrences of: **{search_text}** with: **{replace_with}**")

# File uploader
uploaded_file = st.file_uploader("Choose a JSON file", type=["json"])
if uploaded_file is not None:            
    # Validate it's proper JSON
    try:
        content = uploaded_file.getvalue().decode("utf-8")
        json_data = json.loads(content)
        st.success("Valid JSON file detected")
        
        # Show original data
        with st.expander("Original JSON data"):
            st.json(json_data)
        
        # Perform replace
        new_content = content.replace(search_text, replace_with)
        modified_json = json.loads(new_content)
        
        # Count replacements
        occurrences = content.count(search_text)
        
        # Show results
        st.write(f"**Replaced {occurrences} occurrences**")
        
        with st.expander("Modified JSON data"):
            st.json(modified_json)
        
        # Download button for modified file
        st.download_button(
            label="Download modified JSON",
            data=new_content,
            file_name=f"modified_{uploaded_file.name}",
            mime="application/json"
        )
        
    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid JSON file.")
        