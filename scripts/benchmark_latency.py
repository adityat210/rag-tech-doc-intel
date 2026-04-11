import statistics
import time

from app.services.retriever import Retriever
from app.services.generator import Answers

QUERIES = [
    "how does the essay argue that Simba follows a ritual rite of passage?",
    "what parallels does the paper draw between Simba and Greek myths like Hermes and Io?",
    "why does the paper argue that media turns truth into entertainment and distraction?",
    "how does the essay use Brave New World and John the Savage to discuss truth and irrelevance?",
    "how does the research paper describe AI's impact on education and the workforce?",
    "what methodology does the AP research paper use to study AI in education?",
    "how does the philosophy paper explain happiness through hedonism?",
    "what does the paper say about pleasure and pain in determining happiness?"
]

def main():
    retriever = Retriever()
    generator = Answers()

    latencies = []

    for query in QUERIES:
        start_time = time.time()

        retrieved_ = retriever.retrieve(query, top_k=3)
        answer = generator.generate_(query, retrieved_)

        latency_seconds = round(time.time() - start_time, 3)
        latencies.append(latency_seconds)

        print(f"query: {query}")
        print(f"answer: {answer['answer']}")
        print(f"latency in sec: {latency_seconds}")
        print("-" * 80)

    print()
    print("latency stats:")
    print("=" * 80)
    print(f"# of queries: {len(latencies)}")
    #print(latencies), correctly calculating stats, zeroes showing up
    print("avg latency: {0:.4f} seconds".format(sum(latencies) / len(latencies)))
    print("median latency: {0:.4f} seconds".format(statistics.median(latencies)))
    print("min latency: {0:.4f} seconds".format(min(latencies)))
    print("max latency: {0:.4f} seconds".format(max(latencies)))

if __name__ == "__main__":
    main()