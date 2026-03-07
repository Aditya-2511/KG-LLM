from SPARQLWrapper import SPARQLWrapper, JSON
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# get API key
groq_api_key = os.getenv("GROQ_API_KEY")

sparql = SPARQLWrapper("http://localhost:7200/repositories/company_kg")

sparql.setQuery("""
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
}
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["s"]["value"], result["p"]["value"], result["o"]["value"])


client = OpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)

context = str(results)

question = "Explain the relationship between entities in the graph"

response = client.responses.create(
    model="openai/gpt-oss-20b",
    input=f"Based on this knowledge graph data:\n{context}\nAnswer the question:\n{question}"
)

print(response.output_text)