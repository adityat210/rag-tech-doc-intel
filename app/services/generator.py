from typing import Dict, List
from transformers import pipeline

class Answers:
    #gnerate answers from retrieved chunks using pretrained local hugging face model
    def __init__(self, model_name: str = "google/flan-t5-base"):
        self.generator = pipeline("text2text-generation", model=model_name)
    
    def build_context(self, retrieved_chunks: List[Dict[str,object]]):
        #format the retrieved into prompt-ready context block
        context_ = []
        for chunk in retrieved_chunks:
            citation = chunk["metadata"]["citation"]
            text = chunk["chunk_text"]

            context_.append("source: {0}\n{1}".format(citation, text))
        return "\n\n".join(context_)
    
    def generate_(self, question: str, retrieved_: List[Dict[str, object]]):
        context = self.build_context(retrieved_)
        prompt = ("Answer the question using only the context as follows: If the answer is not supported by the context, say that there is not enough information. \n\n"
                  "Question: {0}\n\n" "Context: \n{1}\n\n" "Answer:").format(question,context)
        output = self.generator(prompt, max_new_tokens=150, do_sample=False)
        answer_text = output[0]["generated_text"].strip()
        citations = []
        seen = set()

        for chunk in retrieved_:
            citation = chunk["metadata"]["citation"]
            if citation not in seen:
                citations.append(citation)
                seen.add(citation)
        
        return {
            "answer": answer_text,
            "citations": citations,
            "context_count": len(retrieved_)
        }