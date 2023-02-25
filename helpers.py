"""
calculate_freq:
    orders an array of arrays by iterating over each array and iterating over each array's element
    if an element is already a key in the dictionary, it adds 1 to its value
    else, it is appended to the dict and its value is set to 1
    it then returns the sorted dict (reverse means in descending order)
"""
def calculate_freq(tags: list) -> list:
    count = {}
    for i in tags:
        for e in i:
            if count.get(e) is None:
                count[e] = 1
            else:
                count[e] += 1        
        
    return sorted(count.items(), key=lambda x: x[1], reverse=True)


"""
top_tags:
    just a bit of list comprehension, returns word of the most popular tags
"""
def top_tags(tags: list) -> list:
    return [i[0] for i in tags[0:5]]
