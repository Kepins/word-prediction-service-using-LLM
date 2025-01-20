import functools
import time
import matplotlib.pyplot as plt
from typing import Literal

import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, pipeline, PreTrainedTokenizerFast, StoppingCriteriaList

from llm.src.main import StopAfterOneFullWord

PROMPTS = [
    "Kocham czytać ",
    "Lubię biegać po ",
    "Czuję radość, gdy słucham ",
    "Pamiętam wspaniałe chwile z ",
    "Chciałbym odwiedzić ",
    "Widzę piękne krajobrazy w tym ",
    "Jem smaczne jedzenie z ",
    "Lubię rozmawiać o ",
    "Czuję się szczęśliwy, gdy ",
    "Kocham oglądać zachody ",
    "Biegam codziennie ",
    "Pamiętam każdą podróż, którą ",
    "Lubię gotować nowe ",
    "Chciałbym poznać nowe ",
    "Widzę w przyszłości wiele ",
    "Czuję spokój, gdy ",
]

def n_prompts(n: int) -> list[str]:
    return [PROMPTS[i % len(PROMPTS)] for i in range(n)]


def test_inference_time(pipe, prompts) -> float:
    prompts_lengths = [len(p) for p in prompts]

    start_time = time.time()
    stopping_criteria = StoppingCriteriaList([StopAfterOneFullWord(pipe.tokenizer, prompts_lengths)])

    responses = pipe(
        prompts,
        stopping_criteria=stopping_criteria,
    )
    duration = time.time() - start_time
    return duration / len(prompts)


def test_batch_sizes(model, tokenizer) -> list[dict]:
    prompts = n_prompts(10240)
    results = []
    for batch_size in (1, 2, 4, 8, 16, 32, 64, 128):
        partial_pipe = functools.partial(
            pipeline,
            task='text-generation',
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=20, # Limit to 20 tokens
        )

        if batch_size == 1:
            pipe = partial_pipe()
        else:
            pipe = partial_pipe(batch_size=batch_size)
            pipe.tokenizer.pad_token_id = pipe.tokenizer.eos_token_id
        time_per_prompt = test_inference_time(pipe, prompts)
        print(f"{batch_size=} | Time per prompt: {time_per_prompt}")
        results.append({"batch_size": batch_size, "time": time_per_prompt})
    return results


def plot_and_save(results: list[dict], title: str, filepath: str) -> None:
    # Extract batch size and time per prompt
    batch_sizes = [result['batch_size'] for result in results]
    times_per_prompt = [result['time'] * 1000 for result in results]

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(batch_sizes, times_per_prompt, marker='o', linestyle='-', color='b')
    plt.xlabel("Batch Size")
    plt.ylabel("Time per Prompt (ms)")
    plt.title(title)
    plt.grid(True)
    # plt.xlim(0, 1050)
    plt.ylim(0, 40)
    plt.xscale('log')  # Log scale for batch size
    # plt.yscale('log')  # Log scale for time

    # Save the plot to the specified file path
    plt.savefig(filepath)
    plt.close()  # Close the plot to release memory


def load_model(model_id: Literal["Qra-1B", "Llama-3.2-1B"]):
    match model_id:
        case "Qra-1B":
            model_id = f'./llm/resources/models/Qra-1B'
            model = LlamaForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map=0)
            tokenizer = LlamaTokenizer.from_pretrained(model_id, padding_side='left')
            # To get rid of warning "Setting `pad_token_id` to `eos_token_id`:None for open-end generation."
            model.generation_config.pad_token_id = model.generation_config.eos_token_id
        case "Llama-3.2-1B":
            model_id = './llm/resources/models/Llama-3.2-1B'
            model = LlamaForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map=0)
            tokenizer = PreTrainedTokenizerFast.from_pretrained(model_id, padding_side='left')
            # To get rid of warning "Setting `pad_token_id` to `eos_token_id`:None for open-end generation."
            model.generation_config.pad_token_id = model.generation_config.eos_token_id
        case "Llama-3.2-3B":
            model_id = './llm/resources/models/Llama-3.2-3B'
            model = LlamaForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map=0)
            tokenizer = PreTrainedTokenizerFast.from_pretrained(model_id, padding_side='left')
            # To get rid of warning "Setting `pad_token_id` to `eos_token_id`:None for open-end generation."
            model.generation_config.pad_token_id = model.generation_config.eos_token_id
        case _:
            err_message = f"Unknown model id: {model_id}"
            raise ValueError(err_message)
    return model, tokenizer


def load_model_flash_attention(model_id: Literal["Qra-1B", "Llama-3.2-1B"]):
    match model_id:
        case "Qra-1B":
            model_id = f'./llm/resources/models/Qra-1B'
            model = LlamaForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, attn_implementation='flash_attention_2', device_map=0)
            tokenizer = LlamaTokenizer.from_pretrained(model_id, padding_side='left')
            # To get rid of warning "Setting `pad_token_id` to `eos_token_id`:None for open-end generation."
            model.generation_config.pad_token_id = model.generation_config.eos_token_id
        case "Llama-3.2-1B":
            model_id = './llm/resources/models/Llama-3.2-1B'
            model = LlamaForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, attn_implementation="flash_attention_2", device_map=0)
            tokenizer = PreTrainedTokenizerFast.from_pretrained(model_id, padding_side='left')
            # To get rid of warning "Setting `pad_token_id` to `eos_token_id`:None for open-end generation."
            model.generation_config.pad_token_id = model.generation_config.eos_token_id
        case "Llama-3.2-3B":
            model_id = './llm/resources/models/Llama-3.2-3B'
            model = LlamaForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, attn_implementation="flash_attention_2", device_map=0)
            tokenizer = PreTrainedTokenizerFast.from_pretrained(model_id, padding_side='left')
            # To get rid of warning "Setting `pad_token_id` to `eos_token_id`:None for open-end generation."
            model.generation_config.pad_token_id = model.generation_config.eos_token_id
        case _:
            err_message = f"Unknown model id: {model_id}"
            raise ValueError(err_message)
    return model, tokenizer

if __name__ == "__main__":
    #
    # Qra-1B
    #
    # Load model and tokenizer with flash attention
    qra1b_model_fa, qra1b_tokenizer_fa = load_model_flash_attention("Qra-1B")

    # Get the results of test_batch_sizes
    results = test_batch_sizes(qra1b_model_fa, qra1b_tokenizer_fa)

    # Define the title and file path for saving the plot
    title = "Time per prompt Qra-1B with flash_attention"
    filepath = "./time_per_prompt_qra1b_flash_attention.png"

    # Call the function to plot and save
    plot_and_save(results, title, filepath)
    print(f"Plot saved to {filepath}")

    # Load model and tokenizer without flash attention
    qra1b_model, qra1b_tokenizer = load_model("Qra-1B")
    # Get the results of test_batch_sizes
    results = test_batch_sizes(qra1b_model, qra1b_tokenizer)
    # Define the title and file path for saving the plot
    title = "Time per prompt Qra-1B"
    filepath = "./time_per_prompt_qra1b.png"
    # Call the function to plot and save
    plot_and_save(results, title, filepath)
    print(f"Plot saved to {filepath}")

    #
    # Llama3.2-1B
    #
    # Load model and tokenizer with flash attention
    llama1b_model_fa, llama1b_tokenizer_fa = load_model_flash_attention("Llama-3.2-1B")

    # Get the results of test_batch_sizes
    results = test_batch_sizes(llama1b_model_fa, llama1b_tokenizer_fa)

    # Define the title and file path for saving the plot
    title = "Time per prompt Llama-1B with flash_attention"
    filepath = "./time_per_prompt_llama1b_flash_attention.png"

    # Call the function to plot and save
    plot_and_save(results, title, filepath)
    print(f"Plot saved to {filepath}")

    # Load model and tokenizer without flash attention
    llama1b_model, llama1b_tokenizer = load_model("Llama-3.2-1B")

    # Get the results of test_batch_sizes
    results = test_batch_sizes(llama1b_model, llama1b_tokenizer)

    # Define the title and file path for saving the plot
    title = "Time per prompt Llama-1B"
    filepath = "./time_per_prompt_llama1b.png"

    # Call the function to plot and save
    plot_and_save(results, title, filepath)
    print(f"Plot saved to {filepath}")

    #
    # Llama3.2-3B
    #
    # Load model and tokenizer with flash attention
    llama3b_model_fa, llama3b_tokenizer_fa = load_model_flash_attention("Llama-3.2-3B")

    # Get the results of test_batch_sizes
    results = test_batch_sizes(llama3b_model_fa, llama3b_tokenizer_fa)

    # Define the title and file path for saving the plot
    title = "Time per prompt Llama-3.2-3B with flash_attention"
    filepath = "./time_per_prompt_llama3b_flash_attention.png"

    # Call the function to plot and save
    plot_and_save(results, title, filepath)
    print(f"Plot saved to {filepath}")

    # Load model and tokenizer without flash attention
    llama3b_model, llama3b_tokenizer = load_model("Llama-3.2-3B")

    # Get the results of test_batch_sizes
    results = test_batch_sizes(llama3b_model, llama3b_tokenizer)

    # Define the title and file path for saving the plot
    title = "Time per prompt Llama-3.2-3B"
    filepath = "./time_per_prompt_llama3b.png"

    # Call the function to plot and save
    plot_and_save(results, title, filepath)
    print(f"Plot saved to {filepath}")
