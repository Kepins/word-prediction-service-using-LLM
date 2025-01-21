import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    data = [
        {
            "workers": 1,
            "successful_requests": 10240,
            "failed_requests": 0,
            "avg_time_per_prompt_s": 60.4257 / 1000,
            "avg_time_s": 0.0604,
            "std_dev_s": 0.0200,
            "max_time_s": 0.1713,
            "min_time_s": 0.0384
        },
        {
            "workers": 2,
            "successful_requests": 10240,
            "failed_requests": 0,
            "avg_time_per_prompt_s": 58.2312 / 1000,
            "avg_time_s": 0.1164,
            "std_dev_s": 0.0285,
            "max_time_s": 0.2484,
            "min_time_s": 0.0724
        },
        {
            "workers": 4,
            "successful_requests": 10240,
            "failed_requests": 0,
            "avg_time_per_prompt_s": 35.5944 / 1000,
            "avg_time_s": 0.1423,
            "std_dev_s": 0.0313,
            "max_time_s": 0.2615,
            "min_time_s": 0.0786
        },
        {
            "workers": 8,
            "successful_requests": 10240,
            "failed_requests": 0,
            "avg_time_per_prompt_s": 21.1380 / 1000,
            "avg_time_s": 0.1690,
            "std_dev_s": 0.0335,
            "max_time_s": 0.2692,
            "min_time_s": 0.0878
        },
        {
            "workers": 16,
            "successful_requests": 10240,
            "failed_requests": 0,
            "avg_time_per_prompt_s": 13.9174 / 1000,
            "avg_time_s": 0.2225,
            "std_dev_s": 0.0335,
            "max_time_s": 0.3080,
            "min_time_s": 0.0762
        },
        {
            "workers": 32,
            "successful_requests": 10240,
            "failed_requests": 0,
            "avg_time_per_prompt_s": 9.4464 / 1000,
            "avg_time_s": 0.3019,
            "std_dev_s": 0.0343,
            "max_time_s": 0.3714,
            "min_time_s": 0.0934
        },
        {
            "workers": 64,
            "successful_requests": 10240,
            "failed_requests": 0,
            "avg_time_per_prompt_s": 7.0053 / 1000,
            "avg_time_s": 0.4469,
            "std_dev_s": 0.0312,
            "max_time_s": 0.4936,
            "min_time_s": 0.0732
        },
        {
            "workers": 128,
            "successful_requests": 10240,
            "failed_requests": 0,
            "avg_time_per_prompt_s": 5.4495 / 1000,
            "avg_time_s": 0.6945,
            "std_dev_s": 0.0239,
            "max_time_s": 0.8233,
            "min_time_s": 0.1209
        },
        {
            "workers": 256,
            "successful_requests": 10240,
            "failed_requests": 0,
            "avg_time_per_prompt_s": 5.5655 / 1000,
            "avg_time_s": 1.4098,
            "std_dev_s": 0.1167,
            "max_time_s": 1.9166,
            "min_time_s": 0.1312
        },
        {
            "workers": 512,
            "successful_requests": 10240,
            "failed_requests": 0,
            "avg_time_per_prompt_s": 5.5620 / 1000,
            "avg_time_s": 2.7808,
            "std_dev_s": 0.3098,
            "max_time_s": 2.8837,
            "min_time_s": 0.0731
        },
        {
            "workers": 1024,
            "successful_requests": 10240,
            "failed_requests": 0,
            "avg_time_per_prompt_s": 5.8083 / 1000,
            "avg_time_s": 5.6600,
            "std_dev_s": 0.9631,
            "max_time_s": 6.7586,
            "min_time_s": 0.0929
        }
    ]

    # Extract data
    workers = [entry["workers"] for entry in data]
    avg_time_s = [entry["avg_time_s"] for entry in data]
    avg_time_per_prompt_s = [entry["avg_time_per_prompt_s"] for entry in data]
    std_dev_s = [entry["std_dev_s"] for entry in data]
    min_time_s = [entry["min_time_s"] for entry in data]
    max_time_s = [entry["max_time_s"] for entry in data]

    # Calculate bounds for avg ± std_dev
    avg_minus_std = [avg - std for avg, std in zip(avg_time_s, std_dev_s)]
    avg_plus_std = [avg + std for avg, std in zip(avg_time_s, std_dev_s)]

    # Plot
    plt.figure(figsize=(12, 8))

    # Plot the range (min to max) as bars
    plt.fill_between(workers, min_time_s, max_time_s, color='lightblue', alpha=0.5, label="Range (Min to Max)")

    # Plot the range (avg ± std_dev) as bars
    plt.fill_between(workers, avg_minus_std, avg_plus_std, color='lightgreen', alpha=0.5, label="Range (Avg ± Std Dev)")

    # Plot the average time as a line
    plt.plot(workers, avg_time_s, label="Average Time (s)", color="blue", marker="o", linewidth=2)

    # Plot the average time per prompt as a line
    plt.plot(workers, avg_time_per_prompt_s, label="Avg Time per Prompt (s)", color="orange", marker="x", linestyle="--", linewidth=2)

    # Configure plot
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of Workers (log scale)")
    plt.ylabel("Response Time (s) (log scale)")
    plt.title("Response Time Metrics vs Number of Workers")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()

    # Show plot
    plt.savefig("stress-test-plot.png")
    plt.close()
