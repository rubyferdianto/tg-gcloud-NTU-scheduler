from transformers import pipeline

class HuggingFaceClient:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.nlp = pipeline("fill-mask", model=model_name)

    def predict(self, text: str):
        # Example: text = "The capital of France is [MASK]."
        return self.nlp(text)