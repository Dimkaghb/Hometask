"""Dataset generation script.

Loads the dataset from HuggingFace and saves to local JSONL files.

Usage:
    python -m data.generate_dataset
"""

import json
from pathlib import Path

from datasets import load_dataset


def main():
    output_dir = Path(__file__).parent.resolve()
    
    print("Loading dataset from HuggingFace...")
    ds = load_dataset("myxik/KazOAI-2026-HomeTask")
    
    train_samples = []
    for item in ds["train"]:
        train_samples.append({
            "input": item["input"],
            "output": item["output"],
            "format": item["format"],
        })
    
    train_path = output_dir / "train.jsonl"
    print(f"Writing {len(train_samples)} training samples to {train_path}")
    with open(train_path, "w", encoding="utf-8") as f:
        for sample in train_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
    
    test_path = output_dir / "test.jsonl"
    test_ground_truth_path = output_dir / "test_ground_truth.jsonl"
    
    test_samples = []
    test_ground_truth = []
    
    for item in ds.get("test", []):
        test_samples.append({
            "input": item["input"],
            "format": item["format"],
        })
        test_ground_truth.append({
            "input": item["input"],
            "output": item["output"],
            "format": item["format"],
        })
    
    if test_samples:
        print(f"Writing {len(test_samples)} test samples to {test_path}")
        with open(test_path, "w", encoding="utf-8") as f:
            for sample in test_samples:
                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
        
        print(f"Writing {len(test_ground_truth)} ground truth samples to {test_ground_truth_path}")
        with open(test_ground_truth_path, "w", encoding="utf-8") as f:
            for sample in test_ground_truth:
                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
    else:
        print("No test split found in dataset")
    
    print("Done!")


if __name__ == "__main__":
    main()
