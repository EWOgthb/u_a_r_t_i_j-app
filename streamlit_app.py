import streamlit as st
import json
from io import StringIO

sb_id = st.secrets["sb_id"]
pr_id = st.secrets["pr_id"]

st.info(f"Will replace all resource IDs in json file")

# File uploader
uploaded_file = st.file_uploader("Choose a JSON file", type=["json"])
if uploaded_file is not None:            
    # Validate it's proper JSON
    try:
        content = uploaded_file.getvalue().decode("utf-8")
        json_data = json.loads(content)
        st.success("Valid JSON file detected")
        
        # Show original data
        #with st.expander("Original JSON data"):
        #  st.json(json_data)
        
        sb_count=content.count(sb_id)
        pr_count=content.count(pr_id)
        new_file_name=f"converted_{ "to_PROD"if sb_count>0 else "to_Sandbox"}"
        if sb_count > 0:
            new_content = content.replace(sb_id, pr_id)
            st.write(f"**{sb_count} Sandbox Resource ID replaced with Prod ID**")
        elif pr_count > 0:
            new_content = content.replace(pr_id, sb_id)
            st.write(f"**{pr_count} Prod ID Resource ID replaced with Sandbox ID**")
        else:
            raise FileNotFoundError
        
        modified_json = json.loads(new_content)
                
        #with st.expander("Modified JSON data"):
        #   st.json(modified_json)
        
        # Download button for modified file
        st.download_button(
            label="Download modified JSON",
            data=new_content,
            file_name=new_file_name,
            mime="application/json"
        )
        
    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid JSON file.")
    except FileNotFoundError:
        st.error("Json file doesn't contain Sandbox or Prod ID!")
        