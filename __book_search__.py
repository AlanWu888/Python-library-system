import __database__ as DB

def findInDatabase(field_to_search, query):
    database = DB.txtToList()
    list_of_matches = []
    match = ""

    for entry in range(len(database)):
        if database[entry][field_to_search].upper() == query.upper():
            # print(database[entry])
            match = database[entry]
            list_of_matches.append(match)
    # print(list_of_matches)

    return list_of_matches

