import anthropic
import json
import pandas as pd
import pinecone
import time
import voyageai
from tqdm.auto import tqdm

# API keys (replace with your actual keys)
ANTHROPIC_API_KEY = "<YOUR_ANTHROPIC_API_KEY>"
PINECONE_API_KEY = "<YOUR_PINECONE_API_KEY>"
VOYAGE_API_KEY = "<YOUR_VOYAGE_API_KEY>"

def setup_clients():
    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    pinecone_client = pinecone.Pinecone(api_key=PINECONE_API_KEY)
    voyage_client = voyageai.Client(api_key=VOYAGE_API_KEY)
    return anthropic_client, pinecone_client, voyage_client

def load_dataset(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                data.append(eval(line))
            except:
                pass
    return pd.DataFrame(data)

def setup_pinecone_index(pc, index_name, dimension=1024):
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    
    if index_name not in existing_indexes:
        spec = pinecone.ServerlessSpec(cloud="aws", region="us-west-2")
        pc.create_index(
            index_name,
            dimension=dimension,
            metric='dotproduct',
            spec=spec
        )
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
    
    return pc.Index(index_name)

def upload_to_pinecone(index, vo, descriptions, batch_size=100):
    for i in tqdm(range(0, len(descriptions), batch_size)):
        i_end = min(len(descriptions), i+batch_size)
        descriptions_batch = descriptions[i:i_end]
        
        done = False
        while not done:
            try:
                res = vo.embed(descriptions_batch, model="voyage-2", input_type="document")
                done = True
            except:
                time.sleep(5)
        
        embeds = [record for record in res.embeddings]
        ids_batch = [f"description_{idx}" for idx in range(i, i_end)]
        metadata_batch = [{'description': description} for description in descriptions_batch]
        to_upsert = list(zip(ids_batch, embeds, metadata_batch))
        index.upsert(vectors=to_upsert)

def get_completion(client, prompt):
    completion = client.completions.create(
        model="claude-2.1",
        prompt=prompt,
        max_tokens_to_sample=1024,
    )
    return completion.completion

def create_keyword_prompt(question):
    return f"""
Human: Given a question, generate a list of 5 very diverse search keywords that can be used to search for products on Amazon.

The question is: {question}

Output your keywords as a JSON that has one property "keywords" that is a list of strings. Only output valid JSON.
"""

def format_results(extracted: list[str]) -> str:
    result = "\n".join(
        [
            f'<item index="{i+1}">\n<page_content>\n{r}\n</page_content>\n</item>'
            for i, r in enumerate(extracted)
        ]
    )
    
    return f"\n<search_results>\n{result}\n</search_results>"

def create_answer_prompt(results_list, question):
    return f"""
Human: {format_results(results_list)} Using the search results provided within the <search_results></search_results> tags, please answer the following question <question>{question}</question>. Do not reference the search results in your answer.

Assistant:"""

def main():
    anthropic_client, pinecone_client, voyage_client = setup_clients()
    df = load_dataset('amazon-products.jsonl')
    index = setup_pinecone_index(pinecone_client, 'amazon-products')
    upload_to_pinecone(index, voyage_client, df['text'].tolist())
    
    USER_QUESTION = "I want to get my daughter more interested in science. What kind of gifts should I get her?"
    keyword_json = "{" + get_completion(anthropic_client, create_keyword_prompt(USER_QUESTION))
    data = json.loads(keyword_json)
    keywords_list = data['keywords']
    
    results_list = []
    for keyword in keywords_list:
        query_embed = voyage_client.embed([keyword], model="voyage-2", input_type="query")
        search_results = index.query(vector=query_embed.embeddings, top_k=3, include_metadata=True)
        for search_result in search_results.matches:
            results_list.append(search_result['metadata']['description'])
    
    answer = get_completion(anthropic_client, create_answer_prompt(results_list, USER_QUESTION))
    print(answer)

if __name__ == "__main__":
    main()