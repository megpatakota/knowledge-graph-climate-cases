import pandas as pd
from gliner import GLiNER
import spacy
from tqdm.notebook import tqdm
import pickle

custom_spacy_config = {
    "gliner_model": "urchade/gliner_small-v2.1",
    "chunk_size": 250,
    "labels": ["people", "company", "organization", "location", "date", "money"],
    "style": "dep",
    "threshold": 0.5,
    "map_location": "mps",
}
nlp = spacy.blank("en")
nlp.add_pipe("gliner_spacy", config=custom_spacy_config)

df = pd.read_csv("Global-Cases-Export-2024-09-25.csv")

df.columns = df.columns.str.lower().str.replace(" ", "_")
# split at jurisdictions to jurisdictions_country, jurisdictions_region, jurisdictions_type given the > separator. Eg: 'Australia>New South Wales>Land and Environment Court'
# Note: not all rows have all 3 values
df[["jurisdictions_country", "jurisdictions_region", "jurisdictions_type"]] = df[
    "jurisdictions"
].str.split(">", n=2, expand=True)
df.head()
df = df.sample(10)


def split_text_to_chunks(text, chunk_size=250):
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


chunk_nodes = []
chunk_id = 1
for index, row in df.iterrows():
    text_chunks = split_text_to_chunks(row["summary"], 250)
    doc_id = row["id"]
    for chunk in text_chunks:
        chunk_nodes.append({"id": chunk_id, "doc_id": doc_id, "text": chunk})
        chunk_id += 1

# for chunk in chunk_nodes:
#     print(chunk)
chunk_nodes


def get_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append(
            {
                "text": ent.text,
                "start_char": ent.start_char,
                "end_char": ent.end_char,
                "label": ent.label_,
            }
        )
    return entities


entity_nodes = []
entity_id = 1
for chunk in tqdm(chunk_nodes):
    entities = get_entities(chunk["text"])
    for entity in entities:
        entity_nodes.append(
            {
                "id": entity_id,
                "chunk_id": chunk["id"],
                "text": entity["text"],
                "start_char": entity["start_char"],
                "end_char": entity["end_char"],
                "label": entity["label"],
            }
        )
        entity_id += 1

entity_nodes_sample = [node for node in entity_nodes if node["chunk_id"] == 1]
chunk_nodes_sample = [node for node in chunk_nodes if node["id"] == 1]
chunk_nodes_sample, entity_nodes_sample

# save the chunk and entities to pickle
pickle.dump(chunk_nodes, open("./graph_data/chunk_nodes_sample.pkl", "wb"))
pickle.dump(entity_nodes, open("./graph_data/entity_nodes_sample.pkl", "wb"))
