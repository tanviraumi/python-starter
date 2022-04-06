import fasttext
import os
import re

class LanguageDetect:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        model_location = os.path.join(dirname, '../../../../../../../data/lid.176.bin')
        self.model = fasttext.load_model(model_location)

    def strip_label(self, value):
        return value[len("__label__"):]
    
    def predict_language(self, text):
        # remove and consolidate whitespace for fasttext
        content = re.sub('\s+', ' ', text)
        predictions = self.model.predict(content, k=5) # top 5 matching languages

        # mark the primary language for easy lookup and include the full
        # set of predictions as well
        languages = []
        for idx, pred in enumerate(predictions[0]):
            language = self.strip_label(pred)
            languages.append({
                "language": language,
                "confidence": predictions[1][idx],
            })

        return languages