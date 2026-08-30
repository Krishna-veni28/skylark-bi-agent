import streamlit as st
from agent import answer_business_question


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Skylark BI Agent",
    page_icon="📊",
    layout="centered"
)


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("📊 Skylark Business Intelligence Agent")

st.write(
    "Ask questions about sales pipeline, deals, sectors, "
    "work orders, billing, collections, and receivables."
)


# -------------------------------------------------
# QUESTION INPUT
# -------------------------------------------------

question = st.text_input(
    "Ask a business question:",
    placeholder="Example: How is our pipeline looking?"
)


# -------------------------------------------------
# ASK BUTTON
# -------------------------------------------------

if st.button("Ask Agent"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Fetching latest data from Monday.com..."):

            try:

                answer = answer_business_question(question)

                st.subheader("Agent")

                st.write(answer)

            except Exception as e:

                st.error(
                    "Sorry, I couldn't process your question."
                )

                st.caption(
                    "Please check the Monday.com connection "
                    "and try again."
                )


# -------------------------------------------------
# EXAMPLE QUESTIONS
# -------------------------------------------------

st.divider()

st.subheader("Example questions")

st.markdown(
    """
- How is our pipeline looking?
- Which sector has the highest deal value?
- Which deal stage has the highest value?
- How many work orders are completed?
- How much have we collected?
- How much is receivable?
- How much has been billed?
- Give me a leadership summary
"""
)


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "Data is retrieved dynamically from Monday.com. "
    "This prototype is read-only."
)