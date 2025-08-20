from ddgs import DDGS

query = "raspberrypi"
site = "akizukidenshi.com"
full_query = f"site:{site} {query}"

print(f"Testing query: {full_query}")

with DDGS() as ddgs:
    results = ddgs.text(full_query, max_results=5)
    if results:
        for result in results:
            print(f"Title: {result.get('title')}\nURL: {result.get('href')}\n")
    else:
        print("No results found.")

