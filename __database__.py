from datetime import datetime   # used in update log

#CONST_DatabaseDir = "text files\_test_database.txt"
CONST_DatabaseDir = "text files\database.txt"
CONST_LogDir = "text files\Log.txt"

def ISBN_to_Title_author(ISBN):
    ISBN_index = 1
    title_index = 2
    author_index = 3

    database = txtToList()

    for i in range(len(database)):
        if ISBN == database[i][ISBN_index]:
            string_to_return = database[i][author_index] + ", " + database[i][title_index]

    return string_to_return

def getLog():
    """
    :return: list of the log entries
    """
    logRecord = open(CONST_LogDir, "r")
    listOfAllEntries = []
    for entry in logRecord:
        listOfAllEntries.append(entry)
    logRecord.close()
    return listOfAllEntries

def spaceDatabase(Entry):
    ID = Entry[0]
    ISBN = Entry[1]
    Title = Entry[2]
    Author = Entry[3]
    PurchaseDate = Entry[4]
    MemberID = Entry[5]
    NumberTimesBorrowed = Entry[6]
    to_return = "{:^6}".format(ID) + "║" + "{:^15}".format(ISBN) + "║" + "{:^30}".format(Title) + "║" + "{:^25}".format(Author) + "║" + "{:^17}".format(PurchaseDate) + "║" + "{:^13}".format(MemberID) + "||" + "{:^13}".format(NumberTimesBorrowed)
    return to_return

def txtToList():
    """
This code makes a list of each line of the database each line in my database is an entry for another book.
By creating this list, I can then search for a book and ammend any field in the database if neccessary

code was taken from https://www.kite.com/python/answers/how-to-convert-each-line-in-a-text-file-into-a-list-in-python
    """

    database = open(CONST_DatabaseDir, "r")

    listOfAllEntries = []
    for entry in database:
        stripped_line = entry.strip()
        line_list = stripped_line.split(" || ")
        listOfAllEntries.append(line_list)
    database.close()
    return listOfAllEntries

def get_book_str(BookID):
    database = txtToList()
    CONST_bookID_index = 0
    entry_return = []

    for entry in range(len(database)):
        if database[entry][CONST_bookID_index] == BookID:
            entry_return = database[entry]

    # print(entry_return)

    return entry_return

def update_database(updated_list):
    print("Database updating")
    file = open(CONST_DatabaseDir, "w")

    for entry in range(len(updated_list)):
        line_to_write = (" || ".join(updated_list[entry])) + "\n"
        file.write(line_to_write)
    file.close()

def update_log(access, entry_modified):
    """
This subroutine has been designed to update the log which keeps a track of when a book has been returned or
whenever a book has been checked out
    """
    Space = "\n    "
    NewLine = "=================================================================================================== \n"
    AllowedAccess = ["CheckOut", "Return", "AddBook", "Weeding"]

    CONST_BookID_index = 0
    CONST_ISBN_index = 1
    CONST_Title_index = 2
    CONST_Author_index = 3
    CONST_User_index = 5

    if access in AllowedAccess:
        if access == "CheckOut":
            TypeToWrite = "BOOK CHECKED OUT "
        elif access == "Return":
            TypeToWrite = "BOOK RETURNED    "
        elif access == "AddBook":
            TypeToWrite = "BOOK ADDED       "
        elif access == "Weeding":
            TypeToWrite = "BOOK REMOVED     "

    # Date and time in the form dd/mm/YYYY Hour:Min:Secs
    TimeNow = datetime.now()
    dt_string = TimeNow.strftime("%d/%m/%Y %H:%M:%S")

    ISBN = "Book ISBN:     " + str(entry_modified[
                                       CONST_ISBN_index])  # these are the positions in the list to search in the list which is passed in as a parameter
    User = "Member ID:     " + str(
        entry_modified[CONST_User_index])  # I have done this so that the log can be easily read by the librarian
    BookID = "Book ID:       " + str(entry_modified[CONST_BookID_index])
    TitleAndAuthor = "Book & Author: " + str(entry_modified[CONST_Title_index]) + ", " + str(
        entry_modified[CONST_Author_index])

    LineToAdd = TypeToWrite + dt_string + Space + User + Space + BookID + Space + TitleAndAuthor + Space + ISBN + "\n" + NewLine

    SystemLog = open(CONST_LogDir, "a")
    SystemLog.write(LineToAdd)
    SystemLog.close()

def validID(input):
    valid_length = False
    valid_chars = True
    allowed_chars = "1234567890"

    if len(input) == 4:
        valid_length = True

    for char in range(len(input)):
        if input[char] not in allowed_chars:
            valid_chars = False

    if (valid_length == True) and (valid_chars == True):
        return True
    else:
        return False
