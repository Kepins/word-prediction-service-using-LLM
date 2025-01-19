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
# for sentences.txt == 647.4861425591537
print("Llama mean perplexity:", results_llama["mean_perplexity"])
# for sentences.txt == 2131.36
print(f"Llama computation time: {end_time - start_time:.2f} seconds")

# Measure time for Llama model
start_time = time.time()
results_llama3b = perplexity.compute(
    model_id='meta-llama/Llama-3.2-3B',
    add_start_token=False,
    predictions=input_texts,
    batch_size=1,
)
end_time = time.time()
# for sentences.txt == 401.10
print("Llama-3B mean perplexity:", results_llama3b["mean_perplexity"])
# for sentences.txt == 4534.38
print(f"Llama-3B computation time: {end_time - start_time:.2f} seconds")

# Measure time for Qra model
start_time = time.time()
results_qra = perplexity.compute(
    model_id='OPI-PG/Qra-1b',
    add_start_token=False,
    predictions=input_texts,
    batch_size=3,
)
end_time = time.time()
# for sentences.txt == 78.56059269329432
print("Qra mean perplexity:", results_qra["mean_perplexity"])
# for sentences.txt == 1615.16
print(f"Qra computation time: {end_time - start_time:.2f} seconds")
