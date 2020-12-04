from tkinter import *
from tkinter import ttk

import sys
sys.path.append("modules")
import __database__ as DB, __book_search__ as BS, __book_checkout__ as BC, __book_return__ as BR, __book_weed__ as BW

# region Book search functions
def find_book(access, query):
    if access == "ID":
        position_to_search = 0

    elif access == "ISBN":
        position_to_search = 1

    elif access == "title":
        position_to_search = 2

    elif access == "author":
        position_to_search = 3

    list_matches = BS.findInDatabase(position_to_search, query)
    if len(list_matches) != 0:
        display_matches(list_matches)
    else:
        display_no_matches()

"""
For the four search_by functions below:
    I did try to use only the find_book function where it accepts one parameter but that kept throwing errors, so instead
    I have opted to just use four separate feeder subroutines to help me get around this. 
        >search_by_bookID
        >search_by_ISBN
        >search_by_title
        >search_by_author
"""
def search_by_bookID():
    """
    Add error messages maybe?
                error_invalid.place(x=150, y=50)
                error_empty.place(x=10, y=50)
    """
    allowed_chars = ["1","2","3","4","5","6","7","8","9","0"]
    count_not_allowed = 0
    query = bookquery.get()
    if len(query) != 0:
        for i in range(0, len(query)):
            if query[i] not in allowed_chars:
                count_not_allowed = count_not_allowed + 1
        if count_not_allowed != 0:
            # print("Error - invalid Book ID provided")
            display_error_search("invalid_input_ID")

    else:
        # print("Error - no input detected")
        display_error_search("no_input")

    if len(query)>0 and count_not_allowed == 0:
        find_book("ID", query)

def search_by_ISBN():
    """
    Add error messages maybe?
                error_invalid.place(x=150, y=50)
                error_empty.place(x=10, y=50)
    """
    allowed_chars = ["1","2","3","4","5","6","7","8","9","0"]
    count_not_allowed = 0
    query = bookquery.get()
    if len(query) != 0:
        for i in range(0, len(query)):
            if query[i] not in allowed_chars:
                count_not_allowed = count_not_allowed + 1
        if count_not_allowed != 0:
            # print("Error - invalid ISBN provided")
            display_error_search("invalid_input_ISBN")
    else:
        # print("Error - no input detected")
        display_error_search("no_input")

    if len(query)>0 and count_not_allowed == 0:
        find_book("ISBN", query)

def search_by_title():
    query = bookquery.get()
    if len(query) != 0:
        find_book("title", query)
    else:
        # print("Error - no input detected")
        display_error_search("no_input")

def search_by_author():
    query = bookquery.get()
    if len(query) != 0:
        find_book("author", query)
    else:
        # print("Error - no input detected")
        display_error_search("no_input")

def display_no_matches():
    my_listbox = Listbox(book_search_listbox_frame,width="630", height="8", bg="white")
    my_listbox.place(x=0, y=0)
    book_search_listbox_frame.pack_forget()
    my_listbox.insert(END, "No matches were found - please try again")

def display_error_search(ErrorType):
    my_listbox = Listbox(book_search_listbox_frame,width="630", height="8", bg="red")
    my_listbox.place(x=0, y=0)
    book_search_listbox_frame.pack_forget()
    if ErrorType == "no_input":
        my_listbox.insert(END, "Error - No input made")
    elif ErrorType == "invalid_input_ID":
        my_listbox.insert(END, "Error - Enter a valid input, Book IDs are numbers")
    elif ErrorType == "invalid_input_ISBN":
        my_listbox.insert(END, "Error - Enter a valid input, ISBN should only be made of numbers")

def display_matches(list_of_matches):
    my_listbox = Listbox(book_search_listbox_frame,width="630",height="8", bg="white")
    my_listbox.place(x=0, y=0)
    book_search_listbox_frame.pack_forget()
    my_listbox.insert(END, "Book ID / ISBN / Title / Author / Purchase Date / Member with book")
    my_listbox.insert(END, "")
    for entry in range(len(list_of_matches)):
        my_listbox.insert(END, DB.spaceDatabase(list_of_matches[entry]))
# endregion

# region database and log functions
def reset_box_frame():
    for widget in box_frame_empty.winfo_children():
        widget.destroy()

def display_database():
    """
    This works but it does not display the database as nicely as I would like
    I have also tried to add scrollbars to this, but it is very broken when I implement it.
    """
    my_listbox = Listbox(box_frame_empty, width="56", height="31", bg="thistle1")
    my_listbox.place(x=0, y=0)
    box_frame_empty.pack_forget()

    allBooks = DB.txtToList()
    # add items to list box
    for entry in range(len(allBooks)):
        my_listbox.insert(END, DB.spaceDatabase(allBooks[entry]))
        # end tells python to add the string to the end of the listbox

def display_logfile():
    my_listbox = Listbox(box_frame_empty, width="56", height="31", bg="thistle1")
    my_listbox.place(x=0, y=0)
    box_frame_empty.pack_forget()

    allLogs = DB.getLog()
    # add items to list box
    for log in range(len(allLogs)):
        my_listbox.insert(END, str(allLogs[log]))
# endregion

# region Book Checkout functions
def book_checkout():
    book_available_for_checkout = BC.isBookAvailable(checkout_bookID.get())

    if book_available_for_checkout == True: # check if the book is available to borrow
        if DB.validID(checkout_memberID_entry.get()) == True:   # check if input ID is valid

            line_display = BC.display_line(DB.get_book_str(checkout_bookID.get())) + str(checkout_memberID.get())
            # This line formats the book being checked out so the librarian can see the system being updated

            BC.check_book_out(checkout_bookID.get(), checkout_memberID.get())
            # This updates the book being checked out in the database

            checkout_listbox = Listbox(book_checkout_success, width="200", height="2", bg="green")
            checkout_listbox.place(x=0, y=0)
            checkout_listbox.insert(END, "Successful checkout!")
            checkout_listbox.insert(END, line_display)

            # update the log to show that the book has been checked out
            DB.update_log("CheckOut", DB.get_book_str(checkout_bookID.get()))
        else:
            line_display = "Member ID is not valid - IDs should be 4 digit long numbers!"

            checkout_listbox = Listbox(book_checkout_success, width="200", height="2", bg="red")
            checkout_listbox.place(x=0, y=0)
            checkout_listbox.insert(END, "Unsuccessful checkout :(")
            checkout_listbox.insert(END, line_display)
    else:
        line_display = "Book you are requesting is currently being borrowed"

        checkout_listbox = Listbox(book_checkout_success, width="200", height="2", bg="red")
        checkout_listbox.place(x=0, y=0)
        checkout_listbox.insert(END, "Unsuccessful checkout :(")
        checkout_listbox.insert(END, line_display)

def book_checkout_reset():
    for widget in book_checkout_success.winfo_children():
        widget.destroy()
# endregion

# region Book Return functions
def book_return():
    book_available_for_return = BR.canBeReturned(return_bookID.get())

    if book_available_for_return == True:
        BR.returnBookToSystem(return_bookID.get())
        # This updates the book being returned in the database and log

        DB.update_log("Return", DB.get_book_str(return_bookID.get()))
        # update the log to log that a given book has been returned

        line_display = BR.display_line(DB.get_book_str((return_bookID.get())))
        # This line formats the book being returned so the librarian can see the system being updated

        checkout_listbox = Listbox(book_return_success, width="200", height="2", bg="green")
        checkout_listbox.place(x=0, y=0)
        checkout_listbox.insert(END, "Successful Return!")
        checkout_listbox.insert(END, line_display)

    else:
        line_display = "That book has not been borrowed"
        # This line formats the book being returned so the librarian can see the system being updated

        checkout_listbox = Listbox(book_return_success, width="200", height="2", bg="red")
        checkout_listbox.place(x=0, y=0)
        checkout_listbox.insert(END, "Unuccessful Return :(")
        checkout_listbox.insert(END, line_display)

def book_return_reset():
    for widget in book_return_success.winfo_children():
        widget.destroy()
# endregion

# region Book weeding functions
def book_weed_click():
    list_low_to_high = BW.sort_popularity()
    ISBN_index = 0
    popularity_index = 1
    space = "                        "
    book_weed_listbox = Listbox(book_weed_listbox_frame, width="105", height="5", bg="pale goldenrod")
    book_weed_listbox.place(x=0,y=0)
    book_weed_listbox.insert(END, "Displaying unpopular titles from most unpopular to least unpopular")
    for items in range(len(list_low_to_high)):
        line_display = DB.ISBN_to_Title_author(list_low_to_high[items][ISBN_index])
        book_weed_listbox.insert(END, str(items + 1) + ". " + line_display + space + "popularity rating - " + str(list_low_to_high[items][popularity_index]))

def book_weed_reset():
    for widget in book_weed_listbox_frame.winfo_children():
        widget.destroy()

# endregion

# region app stuff
app = Tk()
app.geometry("1080x720")
app.title("LBS :: Library booking system")
heading = Label(text="Library booking System", fg="white", bg="navy", width="750", height="2", font=("verdana",18))

heading.pack()
# endregion

# region book weeding
book_weed_colour1 = "gainsboro"
book_weed_colour2 = "grey"
book_weed_colour3 = "white"

book_weed_frame = Frame(app, width="650", height="155", bg=book_weed_colour1)
book_weed_frame.place(x=40, y=490)

book_weed_header = Label(book_weed_frame, text="Book weeding :: suggest titles to remove", width="92", bg="black", fg="white")
book_weed_header.place(x=0, y=0)

book_weed_listbox_frame = Frame(book_weed_frame, width="630", height="82", bg=book_weed_colour3)
book_weed_listbox_frame.place(x=10, y=65)

btn_start_weeding = Button(book_weed_frame, text="start weeding", command=book_weed_click, bg=book_weed_colour2)
btn_start_weeding.place(x=10, y=30)

btn_reset_weeding = Button(book_weed_frame, text="reset", command=book_weed_reset, bg="red")
btn_reset_weeding.place(x=100, y=30)
# endregion

# region book return
book_return_frame_colour1 = "gainsboro"
book_return_frame_colour2 = "grey"
book_return_frame_colour3 = "white"

book_return_frame = Frame(app, width="650", height="90", bg=book_return_frame_colour1)
book_return_frame.place(x=40, y=390)

book_return_success = Frame(book_return_frame, width="320", height="45", bg=book_return_frame_colour1)
book_return_success.place(x=270, y=30)

book_checkout_header = Label(book_return_frame, text="Book Return - enter book ID :: Book IDs can be found in the database or by searching", width="93", bg="black", fg=book_return_frame_colour3)
book_checkout_header.place(x=1, y=1)

bookID_return_text = Label(book_return_frame, text="      Book ID : ", bg=book_return_frame_colour1)
bookID_return_text.place(x=10, y=30)

return_bookID = StringVar()
bookID_return_entry = Entry(book_return_frame, textvariable=return_bookID, width="10")
bookID_return_entry.place(x=80, y=30)

btn_book_return = Button(book_return_frame, text="Return book", command=book_return, bg=book_return_frame_colour2, height="3")
btn_book_return.place(x=170, y=27)

btn_reset_return = Button(book_return_frame, text="Reset", command=book_return_reset, bg="red", height="2")
btn_reset_return.place(x=600, y=30)
# endregion

# region book checkout
book_checkout_frame_colour1 = "gainsboro"
book_checkout_frame_colour2 = "grey"
book_checkout_frame_colour3 = "white"

book_checkout_frame = Frame(app, width="650", height="90", bg=book_checkout_frame_colour1)
book_checkout_frame.place(x=40, y=290)

book_checkout_success = Frame(book_checkout_frame, width="320", height="45", bg=book_checkout_frame_colour1)
book_checkout_success.place(x=270, y=30)

book_checkout_header = Label(book_checkout_frame, text="Book Checkout - enter book ID and Member ID :: Book IDs can be found in the database or by searching", width="93", bg="black", fg=book_checkout_frame_colour3)
book_checkout_header.place(x=1, y=1)

book_ID_checkout_text = Label(book_checkout_frame, text="      Book ID : ", bg=book_checkout_frame_colour1)
book_ID_checkout_text.place(x=10, y=30)

checkout_bookID = StringVar()
checkout_bookID_entry = Entry(book_checkout_frame, textvariable=checkout_bookID, width="10")
checkout_bookID_entry.place(x=80, y=30)

member_ID_checkout_text = Label(book_checkout_frame, text="Member ID : ", bg=book_checkout_frame_colour1)
member_ID_checkout_text.place(x=10, y=60)

checkout_memberID = StringVar()
checkout_memberID_entry = Entry(book_checkout_frame, textvariable=checkout_memberID, width="10")
checkout_memberID_entry.place(x=80, y=60)

btn_book_checkout = Button(book_checkout_frame, text="Check-out", command=book_checkout, bg=book_checkout_frame_colour2, height="3")
btn_book_checkout.place(x=170, y=27)

btn_reset_checkout = Button(book_checkout_frame, text="Reset", command=book_checkout_reset, bg="red", height="2")
btn_reset_checkout.place(x=600, y=30)
# endregion

# region book search
book_search_frame_colour1 = "gainsboro"
book_search_frame_colour2 = "grey"
book_search_frame_colour3 = "white"

book_search_frame = Frame(app, width="650", height="200",bg=book_search_frame_colour1)
book_search_frame.place(x=40, y=70)

book_search_listbox_frame = Frame(book_search_frame, width="630", height="130", bg=book_search_frame_colour3)
book_search_listbox_frame.place(x=10, y=60)

book_search_header = Label(book_search_frame, text="Book Search - type in query then choose option", width = "90", bg="black", fg=book_search_frame_colour3)
book_search_header.place(x=1, y=1)

book_title_text = Label(book_search_frame, text="Search by:", bg=book_search_frame_colour1)
book_title_text.place(x=200, y=30)

bookquery = StringVar()
book_query_entry = Entry(book_search_frame, textvariable=bookquery, width="30")
book_query_entry.place(x=10, y=30)

btn_search_title = Button(book_search_frame, text="Title", command=search_by_title, width="8", bg=book_search_frame_colour2)
btn_search_title.place(x=360, y=27)

btn_search_author = Button(book_search_frame, text="Author", command=search_by_author, width="8", bg=book_search_frame_colour2)
btn_search_author.place(x=430, y=27)

btn_search_ISBN = Button(book_search_frame, text="ISBN", command=search_by_ISBN, width="8", bg=book_search_frame_colour2)
btn_search_ISBN.place(x=500, y=27)

btn_search_ID = Button(book_search_frame, text="Book ID", command=search_by_bookID, width="8", bg=book_search_frame_colour2)
btn_search_ID.place(x=570, y=27)
# endregion

# region database and logfile
btn_reset = Button(app, text="reset", bg="red", command=reset_box_frame)
btn_reset.place(x=1000, y=67)

box_frame_empty = Frame(app, width="340", height="500", bg="gainsboro")
box_frame_empty.place(x=700, y=100)

button_prompt_text = Label(text="Press buttons below to display info in above box\nArrow keys can be used to navigate (click first)")
button_prompt_text.place(x=700, y=600)

btn_display_database = Button(app, text="show database", command=display_database, width="12", height="2", fg="black", bg="cyan")
btn_display_database.place(x=950, y=650)

btn_display_logfile = Button(app, text="show log", command=display_logfile, width="12", height="2", fg="black", bg="cyan")
btn_display_logfile.place(x=850, y=650)

reset_text = Label(app, text="This button clears the box below ➜")
reset_text.place(x=800, y=70)
# endregion

mainloop()
