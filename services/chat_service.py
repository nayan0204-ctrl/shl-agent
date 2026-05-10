from retrieval.retrieve import search_assessments


def build_query(messages):

    return " ".join([
        m["content"] for m in messages
        if m["role"] == "user"
    ])


def needs_clarification(messages):

    combined = build_query(messages).lower()

    role_keywords = [
        "developer",
        "engineer",
        "manager",
        "analyst",
        "sales",
        "tester",
        "architect"
    ]

    seniority_keywords = [
        "junior",
        "mid",
        "senior",
        "lead",
        "manager",
        "intern"
    ]

    has_role = any(k in combined for k in role_keywords)

    has_seniority = any(k in combined for k in seniority_keywords)

    return not (has_role and has_seniority)


def is_off_topic(text):

    blocked = [
        "ignore previous instructions",
        "politics",
        "legal advice",
        "terrorism",
        "violence",
        "hack",
        "bypass"
    ]

    text = text.lower()

    return any(b in text for b in blocked)


def is_comparison_query(text):

    comparison_words = [
        "compare",
        "difference",
        "vs",
        "versus"
    ]

    text = text.lower()

    return any(word in text for word in comparison_words)


def handle_comparison(query):

    query = query.lower()

    if "opq" in query and "gsa" in query:

        return {
            "reply": (
                "OPQ32r is a personality assessment measuring behavioral style "
                "and workplace preferences, while General Ability Screen (GSA) "
                "evaluates cognitive and reasoning ability."
            ),
            "recommendations": [],
            "end_of_conversation": True
        }

    return {
        "reply": "Please specify which SHL assessments you want compared.",
        "recommendations": [],
        "end_of_conversation": False
    }


def chat(messages):

    latest_user = messages[-1]["content"]

    # Refuse off-topic
    if is_off_topic(latest_user):

        return {
            "reply": (
                "I can only assist with SHL assessment recommendations "
                "and comparisons."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # Handle comparisons
    if is_comparison_query(latest_user):

        return handle_comparison(latest_user)

    # Clarify vague queries
    if needs_clarification(messages):

        return {
            "reply": (
                "Please specify the job role, seniority level, "
                "and required skills."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # Build query using FULL conversation history
    query = build_query(messages)

    # Refinement naturally works because full history is used
    results = search_assessments(query)

    recommendations = []

    for r in results[:10]:

        recommendations.append({
            "name": r["name"],
            "url": r["url"],
            "test_type": r["test_type"]
        })

    return {
        "reply": (
            f"Here are {len(recommendations)} SHL assessments "
            f"matching your requirements."
        ),
        "recommendations": recommendations,
        "end_of_conversation": True
    }