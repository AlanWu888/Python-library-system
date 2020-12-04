import __database__ as DB

CONST_bookID_index = 0
CONST_memberID_index = 5

def isBookAvailable(BookID):
    database = DB.txtToList()
    bool_return = False
    matched_entry = []

    for entry in range(len(database)):
        if database[entry][CONST_bookID_index] == BookID:
            if database[entry][CONST_memberID_index] == "0":
                bool_return = True
                break

    return bool_return

def display_line(entry):
    bookID = entry[CONST_bookID_index]
    book_title = entry[2]
    ln_return = "Book " + str(bookID) + " : '" + str(book_title) + "' was lent to member "
    return ln_return

def check_book_out(BookID, next_borrower):
    # print("attempting to update the database")

    database = DB.txtToList()
    line_to_update = 0

    # Find the match in the database; book ID may not be in the right order - safety measure
    for entry in range(len(database)):
        if BookID == database[entry][CONST_bookID_index]:
            line_to_update = entry

    # Update the database
    database[line_to_update][CONST_memberID_index] = str(next_borrower)

    # Insert into database AND update log
    DB.update_database(database)
