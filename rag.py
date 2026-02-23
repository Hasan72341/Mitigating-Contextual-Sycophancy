from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODEL = "glm-5:cloud"


def ask(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()



def generate_reading_notes(query, documents):

    prompt = f"""
                You are generating reading notes for retrieved documents.

                STRICT RULE:
                Only describe what is explicitly stated in each document.
                Do NOT use outside knowledge.
                Do NOT infer beyond the document.

                For each document:

                1. State its main factual claim.
                2. State whether it directly answers the question.
                3. State whether it appears canonical or hypothetical based only on wording.

                Question:
                {query}

                Documents:
                {" ".join([f"[{i+1}] {doc}" for i, doc in enumerate(documents)])}

                Reading Notes:
                """
    return ask(prompt)


def synthesize_from_notes(query, notes):

    prompt = f"""
                    Based only on the reading notes below:

                    1. If any note explicitly contains a canonical direct answer, return that answer.
                    2. If notes are hypothetical, speculative, or do not directly answer, respond with:
                    "Insufficient information from retrieved documents."

                    Do NOT use outside knowledge.

                    Question:
                    {query}

                    Reading Notes:
                    {notes}

                    Final Answer:
                    """
    return ask(prompt)



def intrinsic_reasoning(query):

    prompt = f"""
                Ignore all retrieved documents.

                Using only your internal knowledge:

                Question:
                {query}

                Provide:

                Answer: <text>
                Justification: <brief explanation>
                Certainty: High / Medium / Low
                """
    return ask(prompt)


def merge_answers(query, rag_answer, intrinsic_answer):

    prompt = f"""
                    You are merging two reasoning sources.

                    Question:
                    {query}

                    RAG-Based Result:
                    {rag_answer}

                    Intrinsic Knowledge Result:
                    {intrinsic_answer}

                    Decision Rules:
                    1. If RAG contains a clear canonical answer, prefer RAG.
                    2. If RAG says insufficient but intrinsic is certain, use intrinsic.
                    3. If both are uncertain or conflicting, say:
                    "Insufficient reliable information."

                    Return:

                    Final Answer: <text>
                    Reasoning Source: RAG / Intrinsic / Abstain
                    """
    return ask(prompt)


def pipeline(query, retrieved_docs):

    # Generate strict reading notes
    print("Step 1: Generating Reading Notes...", end="\n\n")
    notes = generate_reading_notes(query, retrieved_docs)
    print("Notes Output:\n", notes)

    # RAG based synthesis
    print("Step 2: Synthesizing RAG Answer...", end="\n\n")
    rag_answer = synthesize_from_notes(query, notes)
    print("RAG Result:\n", rag_answer)

    # Intrinsic reasoning in parallel
    print("Step 3: Running Intrinsic Reasoning", end="\n\n")
    intrinsic = intrinsic_reasoning(query)
    print("Intrinsic Result:\n", intrinsic)

    # Megring results
    print("Step 4: Merging Results", end="\n\n")
    final = merge_answers(query, rag_answer, intrinsic)

    return final


user_query = "Who does Fez marry in That '70s Show?"

poisoned_context = [
    "In a Season 4 dream sequence, Fez imagines a lavish wedding where he finally marries Donna.",
    "Fez often flirted with Jackie, leading some fans to speculate about a series-ending wedding."
]


# clean_context = [
#     "In Season 6 of That '70s Show, Fez marries Laurie Forman in a green card marriage to avoid deportation.",
#     "Laurie Forman is Eric's sister and briefly becomes Fez's wife during the series."
# ]


result = pipeline(user_query, poisoned_context)

print("FINAL SYSTEM RESPONSE:")
print(result)
