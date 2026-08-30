from query_engine import answer_query


def answer_business_question(question):
    """
    Answer founder-level business questions using
    the centralized query engine.

    Data is fetched dynamically from Monday.com.
    """

    try:
        return answer_query(question)

    except Exception:
        return (
            "I couldn't retrieve the latest data from Monday.com. "
            "Please check the connection and try again."
        )


# =====================================================
# TEST AGENT
# =====================================================

if __name__ == "__main__":

    print("Skylark Business Intelligence Agent")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower().strip() == "exit":
            break

        try:

            answer = answer_business_question(question)

            print("\nAgent:")
            print(answer)
            print()

        except Exception as e:

            print("\nError:", e)
            print()