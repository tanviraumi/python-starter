import spacy

SPACY_BATCH_SIZE = 10

class EntityDetect:
    def __init__(self):
        self.model = spacy.load("en_core_web_lg")
    
    def predict_entities(self, text):
        doc_entities = self.model(text)
        entities = []

        for ent in doc_entities.ents:
            entities.append({"text": ent.text, "label_": ent.label})

        return {"message": text, "entities":  entities}