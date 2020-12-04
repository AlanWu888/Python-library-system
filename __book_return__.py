import __database__ as DB

CONST_bookID_index = 0
CONST_memberID_index = 5

def canBeReturned(BookID):
    database = DB.txtToList()
    bool_return = False
    matched_entry = []

    for entry in range(len(database)):
        if database[entry][CONST_bookID_index] == BookID:
            if database[entry][CONST_memberID_index] != "0":
                bool_return = True
                break

    return bool_return

def returnBookToSystem(BookID):
    # print("attempting to update the database")

    database = DB.txtToList()
    line_to_update = 0

    # Find the match in the database; book ID may not be in the right order - safety measure
    for entry in range(len(database)):
        if BookID == database[entry][CONST_bookID_index]:
            line_to_update = entry

    # Update the database
    database[line_to_update][CONST_memberID_index] = "0"

    # Insert into database AND update log
    DB.update_database(database)

def display_line(entry):
    bookID = entry[CONST_bookID_index]
    memberID = entry[CONST_memberID_index]
    book_title = entry[2]
    ln_return = "Book " + str(bookID) + " : '" + str(book_title) + "' was returned from member " + memberID
    return ln_return
