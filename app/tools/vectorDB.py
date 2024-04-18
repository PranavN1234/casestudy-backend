from pinecone import Pinecone
from app.tools.openai import get_embedding
import os
import re
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

pc = Pinecone(api_key=PINECONE_API_KEY)

def get_most_similar_chunks_for_query(query, recent_queries, index_name):
    combined_query = " | ".join(recent_queries[-2:] + [query])
    print(f'Combined Query: {combined_query}')
    print("\nEmbedding query using OpenAI ...")
    question_embedding = get_embedding(combined_query)

    print("\nQuerying Pinecone index ...")
    print("\nIndex name:", index_name)
    index = pc.Index(name=index_name)  # Ensure correct initialization of the Pinecone Index

    # Find all part numbers in the query
    part_numbers = re.findall(r'PS\d+', combined_query)
    combined_results = []

    if part_numbers:
        print(f"Filtering for part numbers: {part_numbers}")
        filter_query = {"part_select_number": {"$in": part_numbers}}
        filtered_query_results = index.query(vector=question_embedding, top_k=3, include_metadata=True, filter=filter_query)
        filtered_results = [x['metadata']['description'] for x in filtered_query_results['matches'] if 'description' in x['metadata']]
        combined_results.extend(filtered_results)

    # Perform a general query without filters
    general_query_results = index.query(vector=question_embedding, top_k=3, include_metadata=True)
    all_results = [x['metadata']['description'] for x in general_query_results['matches'] if 'description' in x['metadata']]


    # Combine results, ensuring no duplicates
    for result in all_results:
        if result not in combined_results:
            combined_results.append(result)


    return combined_results