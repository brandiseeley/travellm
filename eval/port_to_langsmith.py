import json
from langsmith import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def port_synthetic_dataset_to_langsmith():
    """
    Port the synthetic dataset from JSON to Langsmith for evaluation.
    """
    # Initialize Langsmith client
    client = Client()
    
    # Dataset configuration
    dataset_name = "Time Travel LM Synthetic Data"
    dataset_description = "Synthetic questions and answers for evaluating time travel language model performance on 1861 historical data"
    
    # Load the synthetic dataset
    with open("../data/synthetic_dataset.json", "r") as f:
        dataset = json.load(f)
    
    print(f"Loading {len(dataset)} examples from synthetic dataset...")
    
    # Create the dataset in Langsmith
    try:
        langsmith_dataset = client.create_dataset(
            dataset_name=dataset_name,
            description=dataset_description
        )
        print(f"Created dataset: {langsmith_dataset.name} (ID: {langsmith_dataset.id})")
    except Exception as e:
        print(f"Dataset may already exist or error occurred: {e}")
        # Try to get existing dataset
        datasets = client.list_datasets()
        langsmith_dataset = None
        for ds in datasets:
            if ds.name == dataset_name:
                langsmith_dataset = ds
                print(f"Using existing dataset: {ds.name} (ID: {ds.id})")
                break
        
        if not langsmith_dataset:
            raise Exception("Could not create or find dataset")
    
    # Port each example to Langsmith
    for i, data_row in enumerate(dataset):
        try:
            # Create example in Langsmith
            example = client.create_example(
                inputs={
                    "question": data_row["user_input"]
                },
                outputs={
                    "answer": data_row["reference"]
                },
                metadata={
                    "context": data_row["reference_contexts"],
                    "synthesizer_name": data_row["synthesizer_name"]
                },
                dataset_id=langsmith_dataset.id
            )
            print(f"Created example {i+1}/{len(dataset)}: {example.id}")
            
        except Exception as e:
            print(f"Error creating example {i+1}: {e}")
            continue
    
    print(f"Successfully ported {len(dataset)} examples to Langsmith dataset: {langsmith_dataset.name}")
    return langsmith_dataset

if __name__ == "__main__":
    port_synthetic_dataset_to_langsmith() 