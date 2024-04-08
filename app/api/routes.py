import os
from . import api_blueprint
from flask import request, jsonify, current_app

from app.tools import openai, vectorDB
from app.utils.embedPrompt import build_prompt
from flask_cors import CORS, cross_origin


PINECONE_INDEX_NAME = 'index235'
recent_queries = []
@api_blueprint.route('/part_query', methods=['POST'])
def handle_query():
    question = request.json['question']

    context_chunks = vectorDB.get_most_similar_chunks_for_query(question, recent_queries, PINECONE_INDEX_NAME)
    prompt = build_prompt(question, context_chunks)

    recent_queries.append(question)
    # keeping the last three queries
    recent_queries[:] = recent_queries[-3:]

    print("\n==== PROMPT ====\n")
    print(prompt)
    answer = openai.get_llm_answer(prompt)
    return jsonify({ "question": question, "answer": answer })
