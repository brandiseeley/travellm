import os
import json

from datasets import load_dataset

YEAR = "1861"
MAX_ARTICLES = 1000

#  Download data for the year 1861 at the associated article level (Default)
dataset = load_dataset("dell-research-harvard/AmericanStories",
    "subset_years",
    year_list=[YEAR]
)

articles = dataset[YEAR]

def save_articles_to_directory(articles, output_dir="data/articles_1861", max_articles=None):
    """Save articles to individual JSON files in the specified directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    for i, article in enumerate(articles):
        if max_articles is not None and i >= max_articles:
            break
        filename = f"article_{i:04d}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(articles) if max_articles is None else max_articles} articles to {output_dir}")

# Save all articles to directory
save_articles_to_directory(articles, output_dir=f"data/articles_{YEAR}_sample", max_articles=MAX_ARTICLES)