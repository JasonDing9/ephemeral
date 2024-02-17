from googlesearch import search

def search_google(query):
    try:
        search_results = search(query, num_results=1)
        first_link = next(search_results, None)
        return first_link

    except Exception as e:
        print(f"An error occurred: {e}")
        return ""