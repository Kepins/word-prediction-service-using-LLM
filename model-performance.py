import evaluate

perplexity = evaluate.load("perplexity", module_type="metric")

with open("sentences-short.txt", "r") as f:
    input_texts = f.readlines()

results_llama = perplexity.compute(
    model_id='meta-llama/Llama-3.2-1B',
    add_start_token=False,
    predictions=input_texts,
    batch_size=3,
)
print(results_llama["mean_perplexity"])  # == 797.4472567111651

results_qra = perplexity.compute(
    model_id='OPI-PG/Qra-1b',
    add_start_token=False,
    predictions=input_texts,
    batch_size=3,
)
print(results_qra["mean_perplexity"])  # == 69.22926830689113