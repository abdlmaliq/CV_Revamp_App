import streamlit as st
import google.generativeai as genai
import os

def get_api_key():
    """Retrieve the API key from environment variable or Streamlit secrets."""
    return os.environ.get("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

def initialize_gemini():
    """Initialize the Gemini AI with error handling."""
    api_key = get_api_key()
    if not api_key:
        st.error("Google API key is not set. Please set the GOOGLE_API_KEY environment variable or add it to your Streamlit secrets.")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

# Initialize Gemini AI
model = initialize_gemini()

def update_cv(cv_text, job_description, custom_instructions):
    prompt = f"""
    As an expert CV editor, please revamp the following CV to better match the job description provided. 
    Focus on highlighting relevant skills and experiences, and ensure the CV can pass ATS software by incorporating key terms from the job description.

    Original CV:
    {cv_text}

    Job Description:
    {job_description}

    Custom Instructions:
    {custom_instructions}

    Please provide the updated CV content.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error updating CV: {str(e)}")
        return None

def generate_cover_letter(cv_text, job_description, custom_instructions):
    prompt = f"""
    As an expert cover letter writer, please generate a cover letter based on the provided CV and job description. 
    Follow these guidelines:
    - Make it unique and industry-friendly
    - Include numbers and relevant skills
    - Showcase 2 or more of the best experiences relevant to the role
    - Use only industry best practices, avoid biases or opinions
    - Use a clear, concise, and formal tone of voice
    - Keep it under 300 words and ensure it fits on one page
    - Tailor the content to match the job description and highlight relevant skills

    CV:
    {cv_text}

    Job Description:
    {job_description}

    Custom Instructions:
    {custom_instructions}

    Please provide the cover letter content.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating cover letter: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="CV and Cover Letter Generator", layout="wide")

    st.title("CV and Cover Letter Generator")
    st.write("Paste your CV content and the job description to generate tailored documents.")

    # Check if API key is set
    if not get_api_key():
        st.error("Google API key is not set. Please set the GOOGLE_API_KEY environment variable or add it to your Streamlit secrets.")
        st.write("To set the API key:")
        st.code("export GOOGLE_API_KEY=your_api_key_here")
        st.write("Or add it to your Streamlit secrets.toml file:")
        st.code("GOOGLE_API_KEY = 'your_api_key_here'")
        st.stop()

    cv_text = st.text_area("Paste your CV content here", height=300)
    job_description = st.text_area("Paste the job description here")

    custom_cv_instructions = st.text_area("Custom instructions for CV revamp (optional)")
    custom_cl_instructions = st.text_area("Custom instructions for cover letter (optional)")

    if cv_text and job_description:
        if st.button("Generate CV and Cover Letter"):
            with st.spinner("Processing... This may take a few moments."):
                updated_cv = update_cv(cv_text, job_description, custom_cv_instructions)
                cover_letter = generate_cover_letter(cv_text, job_description, custom_cl_instructions)

            if updated_cv and cover_letter:
                st.success("CV and Cover Letter generated successfully!")

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Updated CV Preview")
                    st.text_area("CV Content", updated_cv, height=300)
                    st.download_button(
                        label="Download Updated CV",
                        data=updated_cv,
                        file_name="updated_cv.txt",
                        mime="text/plain"
                    )

                with col2:
                    st.subheader("Cover Letter Preview")
                    st.text_area("Cover Letter Content", cover_letter, height=300)
                    st.download_button(
                        label="Download Cover Letter",
                        data=cover_letter,
                        file_name="cover_letter.txt",
                        mime="text/plain"
                    )
            else:
                st.error("Failed to generate documents. Please try again.")
    else:
        st.info("Please provide your CV content and paste the job description to get started.")

if __name__ == "__main__":
    main()
