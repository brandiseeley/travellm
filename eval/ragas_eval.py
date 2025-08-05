import json
import os
import sys
from datetime import datetime

import pandas as pd
from langchain_openai import ChatOpenAI
from ragas import EvaluationDataset, evaluate, RunConfig
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import (
    Faithfulness,
    LLMContextPrecisionWithReference,
    LLMContextRecall,
    ResponseRelevancy,
)

# Add parent directory to path for local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.rag import graph


def load_synthetic_data(filepath: str) -> list:
    """Load synthetic dataset from JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def create_evaluation_dataset(synthetic_data: list) -> list:
    """Create evaluation dataset from synthetic data."""
    eval_dataset = []
    for item in synthetic_data:
        eval_sample = {
            "question": item["user_input"],
            "ground_truth": item["reference"],
            "contexts": item["reference_contexts"],
        }
        eval_dataset.append(eval_sample)
    return eval_dataset


def process_responses(eval_dataset: list) -> list:
    """Process RAG responses for each evaluation sample."""
    print("Processing responses...")
    total = len(eval_dataset)
    for i, test_row in enumerate(eval_dataset, 1):
        response = graph.invoke({"question": test_row["question"]})
        test_row["response"] = response["response"]
        test_row["retrieved_contexts"] = [
            context.page_content for context in response["local_context"]
        ]
        test_row["user_input"] = test_row["question"]
        test_row["reference"] = test_row["ground_truth"]
        if i % 5 == 0:
            print(f"Ran {i}/{total}...")
    return eval_dataset


def run_evaluation(evaluation_dataset: EvaluationDataset) -> pd.DataFrame:
    """Run RAGAS evaluation with specified metrics."""
    evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))
    custom_run_config = RunConfig(timeout=360)
    
    result = evaluate(
        dataset=evaluation_dataset,
        metrics=[
            Faithfulness(),
            ResponseRelevancy(),
            LLMContextPrecisionWithReference(),
            LLMContextRecall(),
        ],
        llm=evaluator_llm,
        run_config=custom_run_config,
    )
    
    return result.to_pandas()


def save_results(results_df: pd.DataFrame, output_dir: str = "ragas_results") -> str:
    """Save evaluation results to CSV file with timestamp."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/ragas_results_{timestamp}.csv"
    results_df.to_csv(filename, index=False)
    return filename


def main():
    """Main evaluation pipeline."""
    # Load synthetic dataset
    synthetic_data = load_synthetic_data("../data/synthetic_dataset.json")
    
    # Create evaluation dataset
    eval_dataset = create_evaluation_dataset(synthetic_data)
    
    # Process RAG responses
    eval_dataset = process_responses(eval_dataset)
    
    # Create RAGAS evaluation dataset
    evaluation_dataset = EvaluationDataset.from_list(eval_dataset)
    
    # Run evaluation
    results_df = run_evaluation(evaluation_dataset)
    
    # Save results
    filename = save_results(results_df)
    print(f"Results saved to: {filename}")


if __name__ == "__main__":
    main()
