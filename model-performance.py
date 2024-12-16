import evaluate
import time

# Load perplexity metric
perplexity = evaluate.load("perplexity", module_type="metric")

# Read input texts
with open("sentences.txt", "r") as f:
    input_texts = f.readlines()

# Measure time for Llama model
start_time = time.time()
results_llama = perplexity.compute(
    model_id='meta-llama/Llama-3.2-1B',
    add_start_token=False,
    predictions=input_texts,
    batch_size=3,
)
end_time = time.time()
# for sentences-short.txt == 797.4472567111651
# for sentences.txt == 647.4861425591537
print("Llama mean perplexity:", results_llama["mean_perplexity"])
# for sentences-short.txt == 142.00
# for sentences.txt == 1234.45
print(f"Llama computation time: {end_time - start_time:.2f} seconds")

# Measure time for Qra model
start_time = time.time()
results_qra = perplexity.compute(
    model_id='OPI-PG/Qra-1b',
    add_start_token=False,
    predictions=input_texts,
    batch_size=3,
)
end_time = time.time()
# for sentences-short.txt == 69.22926830689113
# for sentences.txt == 78.56059269329432
print("Qra mean perplexity:", results_qra["mean_perplexity"])
# for sentences-short.txt == 91.72
# for sentences.txt == 1181.13
print(f"Qra computation time: {end_time - start_time:.2f} seconds")
