

PROMPT_LIMIT = 3750

def build_prompt(query, recent_queries, context_chunks):

    # create the start and end of the prompt
    recent_questions_formatted = "\n".join(recent_queries)  # Format recent queries into a string
    print(recent_questions_formatted)
    prompt_start = (
            f"Recent questions, answer the next question based on previous questions if you need context:\n{recent_questions_formatted}\n\n" +
            "Answer the question based on the context below and recent questions above. If you don't know the answer based on the context provided below, return just the answer to the question. Redirect the user to use https://www.partselect.com/ if you don't have a good answer.\n\n" +
            "Context:\n"
    )
    prompt_end = f"\n\nQuestion: {query}\nAnswer:"

    # append context chunks until we hit the
    # limit of tokens we want to send to the prompt.
    prompt = ""
    for i in range(1, len(context_chunks)):
        if len("\n\n---\n\n".join(context_chunks[:i])) >= PROMPT_LIMIT:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(context_chunks[:i-1]) +
                prompt_end
            )
            break
        elif i == len(context_chunks)-1:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(context_chunks) +
                prompt_end
            )
    return prompt