

PROMPT_LIMIT = 10000

def build_prompt(query, context_chunks):

    prompt_start = (
            "Answer the question based on the context below and recent questions above. If you don't know the answer based on the context provided below, return just the answer to the question. Redirect the user to use https://www.partselect.com/ if you don't have a good answer.\n\n" +
            "Context:\n"
    )


    prompt_end = f"\n\nQuestion: {query}\nAnswer:"
    prompt = prompt_start

    for chunk in context_chunks:
        if len(prompt + "\n\n---\n\n" + chunk + prompt_end) > PROMPT_LIMIT:
            break
        prompt += "\n\n---\n\n" + chunk


    prompt += prompt_end

    return prompt
