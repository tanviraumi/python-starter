import spacy

SPACY_BATCH_SIZE = 10

class EntityDetect:
    def __init__(self):
        self.model = spacy.load("en_core_web_lg")
    
    def predict_entities(self, batch):
        spacy_batch = [(doc['text'], doc['id']) for doc in batch]

        result = []
        for doc, id in self.model.pipe(spacy_batch, as_tuples=True):
            sentences = [
                {
                    "start": sentence.start_char,
                    "end": sentence.end_char,
                }
                for sentence in doc.sents]

            entities = [
                {
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "label": ent.label_,
                }
                for ent in doc.ents]
            result.append({
                "id": id,
                "sentences": sentences,
                "entities": entities
            })
        return result