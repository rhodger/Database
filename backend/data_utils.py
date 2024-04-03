from thefuzz import process, fuzz

def load(collection) -> dict[str, list[str]]:
    """Loads names and keywords from the provided csv.
    
    Loads names and keywords from the csv located at `filename` - keywords are augmented with names,
    industries, and locations to improve performance when identifying similar entries.
    """

    all_docs = {}
    for doc in collection.find({}, {'company_name': 1, 'industry': 1, 'country': 1, 'keywords': 1}):
        all_docs[doc['company_name']] = doc['company_name'] + ',' + doc['industry'] + ',' + doc['country'] + ',' + doc['keywords']

    return all_docs

def retrieve_profile(collection, target: str) -> list[str]:
        """Retrieves the full data for a given entry."""

        return collection.find_one({'company_name': target})

def search(term: str, data: list[str], min: int = 75) -> list[str]:
    """Finds the most relevant matches for a given company name.
    
    Searches through the loaded data for a given name and returns up to ten matches in order of
    confidence. A minimum confidence must be met - in the case that ten results do not meet this
    criteria less will be returned.

    Args:
        term (str): The search term
        data (list[str]): The names to be searched through
        min (int): The minimum confidence for a match to be considered. Defaults to 75(%)

    Returns:
        list[str]: A 0 <= N <= 10 list of matches.
    """

    # Find (max 10) closest matches to the given term
    found = process.extract(term, data, limit=10)

    relevant = []
    for x in found:
        if int(x[1]) >= min:
            # Only interested in matches with confidence greater than the provided minimum
            relevant.append(x)

    return [x[0] for x in relevant]

def find_similar(target: str, data: dict[str, list[str]], min: int = 70) -> list[str]:
    """Finds similar entries in the database.
    
    Finds up to ten entries in the database who's keywords are sufficiently close to the given
    target's. The minimum level of similarity to be considered a match can be specified. If more
    than 10 results match these criteria, only the 10 most confident are returned.

    Args:
        target (str): The name of the entry to be compared against
        data (dict[str, list[str]]): The other entries in the database, specifically their names and
                                     keywords.
        min (int): The minimum level of similarity required to e considered a relevant match.
                   Defaults to 70(%)
    
    Returns:
        list[str]: A list of names of similar entries
    """

    target_kwords = data[target]

    similarities = []
    for key in data.keys():
        # Find the similarity value for each entry in the database
        similarities.append([key, fuzz.token_set_ratio(target_kwords, data[key])])

    # Sort similarities in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)
    # Remove the first value as it will always be the same as the target
    similarities = similarities[1:]

    close_enough = []
    while len(similarities) > 0 and len(close_enough) < 10 and similarities[0][1] >= min:
        # Select a maximum of ten other entries, and only those that meet the minimum similarity
        # value
        close_enough.append(similarities[0])
        similarities = similarities[1:]

    return close_enough