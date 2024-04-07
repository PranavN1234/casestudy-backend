import os
from . import api_blueprint
from flask import request, jsonify, current_app

from app.tools import openai, vectorDB
from app.utils.embedPrompt import build_prompt
from flask_cors import CORS, cross_origin
from flask import session

PINECONE_INDEX_NAME = 'index238'

@api_blueprint.route('/part_query', methods=['POST'])
def handle_query():
    question = request.json['question']

    if 'recent_queries' not in session:
        print('recent queries not in session so reinitializing')
        session['recent_queries'] = []

    print('recent queries are:', session['recent_queries'])

    context_chunks = vectorDB.get_most_similar_chunks_for_query(question, PINECONE_INDEX_NAME)
    prompt = build_prompt(question, session['recent_queries'], context_chunks)

    session['recent_queries'].append(question)

    session['recent_queries'] = session['recent_queries'][-4:]

    print("\n==== PROMPT ====\n")
    print(prompt)
    answer = openai.get_llm_answer(prompt)
    return jsonify({ "question": question, "answer": answer })
