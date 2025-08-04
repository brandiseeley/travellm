import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class LOCSearchParams:
    """Parameters for Library of Congress Chronicling America search"""
    query: Optional[str] = None
    start_date: Optional[str] = None  # YYYY-MM-DD
    end_date: Optional[str] = None    # YYYY-MM-DD
    location_state: Optional[str] = None
    location_city: Optional[str] = None
    display_level: str = "page"  # "all", "issue", "page"
    search_operation: str = "AND"  # "PHRASE", "AND", "OR", "~5", "~10"
    front_pages_only: bool = False

def search_loc(params: LOCSearchParams, max_results: int = 10) -> Dict[str, Any]:
    """
    Search the Library of Congress Chronicling America collection
    
    Args:
        params: Search parameters
        max_results: Maximum number of results to return
    
    Returns:
        Dictionary containing search results and metadata
    """
    base_url = "https://www.loc.gov/collections/chronicling-america/"
    
    # Build query parameters
    query_params = []
    
    # Required format parameter
    query_params.append("fo=json")
    
    # Add search query if provided
    if params.query:
        if params.search_operation == "PHRASE":
            query_params.append(f'qs="{params.query}"')
        elif params.search_operation in ["~5", "~10"]:
            query_params.append(f'qs={params.query}&ops={params.search_operation}')
        else:
            query_params.append(f'qs={params.query}&ops={params.search_operation}')
    
    # Add date range
    if params.start_date:
        query_params.append(f"start_date={params.start_date}")
    if params.end_date:
        query_params.append(f"end_date={params.end_date}")
    
    # Add location filters
    if params.location_state:
        query_params.append(f"location_state={params.location_state}")
    if params.location_city:
        query_params.append(f"location_city={params.location_city}")
    
    # Add display level
    if params.display_level != "all":
        query_params.append(f"dl={params.display_level}")
    
    # Add front pages only filter
    if params.front_pages_only:
        query_params.append("front_pages_only=true")
    
    # Construct full URL
    query_string = "&".join(query_params)
    url = f"{base_url}?{query_string}"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Limit results if specified
        if max_results and "results" in data:
            data["results"] = data["results"][:max_results]
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from LOC API: {e}")
        return {"results": []}
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")
        return {"results": []}

def search_1861_articles(query: list[str], state: Optional[str] = None, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Convenience function to search for 1861 articles specifically
    
    Args:
        query: Search terms
        state: Optional state filter
        max_results: Maximum number of results
    
    Returns:
        List of article results
    """
    params = LOCSearchParams(
        query="+".join(query),
        start_date="1861-01-01",
        end_date="1861-12-31",
        display_level="page",
        search_operation="AND",
        location_state=state
    )
    
    results = search_loc(params, max_results)
    return results.get("results", [])

def parse_loc_article(article: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a LOC article into a dictionary
    """
    return {
        "title": article["title"],
        "url": article["url"],
        "date": article["date"],
        "description": article["description"],
    }

if __name__ == "__main__":
    # Test basic search
    print("Testing LOC search...")
    
    # Search for fever remedies in 1861
    fever_results = search_1861_articles(["fever", "remedy"], max_results=3)
    print(f"Found {len(fever_results)} articles about fever")

    for article in fever_results:
        print(parse_loc_article(article))
