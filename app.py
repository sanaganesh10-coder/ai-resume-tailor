import streamlit as st
from ai_logic import analyze_resume

st.set_page_config(page_title="AI Resume Tailor", page_icon="📄")

st.title("📄 AI Resume Tailor")
st.write(
    "Paste your resume and a job description. "
    "The app will score your match, list missing keywords, and suggest tailored bullets."
)

# Two text areas
resume_text = st.text_area("Your resume (paste text)", height=250)
jd_text = st.text_area("Job description (paste text)", height=250)

if st.button("Analyze"):
    if not resume_text.strip() or not jd_text.strip():
        st.warning("Please paste both your resume and the job description.")
    else:
        with st.spinner("Analyzing your resume..."):
            try:
                result = analyze_resume(resume_text, jd_text)

                # Ensure we have a dict
                if not isinstance(result, dict):
                    st.error("Unexpected result format from AI.")
                    st.write("Result:", result)
                    result = {}

                match_score = result.get("match_score", 0)
                missing_keywords = result.get("missing_keywords", [])
                tailored_bullets = result.get("tailored_bullets", [])

                st.subheader("Match Score")
                st.metric("Resume–JD Match", f"{match_score}/100")

                st.subheader("Missing Keywords")
                if missing_keywords and isinstance(missing_keywords, list):
                    for kw in missing_keywords:
                        st.write(f"- {kw}")
                else:
                    st.write("No missing keywords detected.")

                st.subheader("Tailored Bullet Suggestions")
                if tailored_bullets and isinstance(tailored_bullets, list):
                    for bullet in tailored_bullets:
                        st.write(f"- {bullet}")
                else:
                    st.write("No bullet suggestions generated.")

            except Exception as e:
                st.error(f"Something went wrong: {e}")