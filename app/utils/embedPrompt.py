

PROMPT_LIMIT = 3750

def build_prompt(query, context_chunks):
    # Format recent queries into a string


    # Create the start of the prompt with instructions to check for follow-up questions
    prompt_start = (
            "Answer the question based on the context below and recent questions above. If you don't know the answer based on the context provided below, return just the answer to the question. Redirect the user to use https://www.partselect.com/ if you don't have a good answer.\n\n" +
            "Context:\n"
    )

    # Append context chunks, keeping an eye on the token limit
    prompt_end = f"\n\nQuestion: {query}\nAnswer:"
    prompt = prompt_start

    for chunk in context_chunks:
        if len(prompt + "\n\n---\n\n" + chunk + prompt_end) > PROMPT_LIMIT:
            break
        prompt += "\n\n---\n\n" + chunk

    # Add the question and the placeholder for the answer at the end
    prompt += prompt_end

    return prompt
