from pinecone import Pinecone
from app.tools.openai import get_embedding
import os

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

pc = Pinecone(api_key=PINECONE_API_KEY)

def get_most_similar_chunks_for_query(query, recent_queries, index_name):

    combined_query = " | ".join(recent_queries[-2:] + [query])
    print(f'Combined Query {combined_query}')
    print("\nEmbedding query using OpenAI ...")
    question_embedding = get_embedding(combined_query)

    print("\nQuerying Pinecone index ...")
    print("\n index name", index_name)
    index = pc.Index(index_name)
    query_results = index.query(vector=question_embedding, top_k=3, include_metadata=True)
    context_chunks = [x['metadata']['description'] for x in query_results['matches']]

    return context_chunks