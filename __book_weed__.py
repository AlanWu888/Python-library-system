import __database__ as DB
from datetime import *

CONST_ISBN_index = 1
CONST_date_index = 4
CONST_borrow_count_index = 6

def popularity_per_title():
    database = DB.txtToList()

    list_of_book_ISBNs = get_list_titles(database)      # list containing unique ISBNs for books
    list_of_combined_borrows = []

    # get the number of borrows for each book as a list
    for ISBNs in range(len(list_of_book_ISBNs)):
        num_borrows = 0
        for books in range(len(database)):
            if database[books][CONST_ISBN_index] == list_of_book_ISBNs[ISBNs]:
                num_borrows = num_borrows + int(database[books][CONST_borrow_count_index])
        # print(list_of_book_ISBNs[ISBNs])
        # print(num_copies)
        # print()
        list_of_combined_borrows.append(num_borrows)

    # get list containing the average number of days since a book was purchased.
    average_days_since_purchase = get_days_since_purchase(database, list_of_book_ISBNs)

    # find average borrows for each book :: (average days since purchase) DIVIDE (number of borrows per book)
    list_ISBN_and_avg_borrows = []
    for book in range(len(list_of_book_ISBNs)):     # cycle through every unique book title in our ISBN list
        pair = []

        curr_borrow_count = list_of_combined_borrows[book]
        curr_average_days = average_days_since_purchase[book]
        # average_borrows tells us how frequently a book is borrowed in days
        average_borrows = curr_borrow_count / curr_average_days

        # print(curr_borrow_count)
        # print(curr_average_days)
        # print(average_borrows)
        # print()

        pair = (list_of_book_ISBNs[book], average_borrows)  # makes a pair list of ISBN and it's book popularity
        # print(book, pair)

        list_ISBN_and_avg_borrows.append(pair)  # add the pair to the list that will be returned

    # print("       ISBN LIST : " + str(list_of_book_ISBNs))
    # print("COMBINED BORROWS : " + str(list_of_combined_borrows))
    # print("    AVERAGE DAYS : " + str(average_days_since_purchase))
    # print("ISBN and avg bor : " + str(list_ISBN_and_avg_borrows))

    return list_ISBN_and_avg_borrows

def sort_popularity():
    """
    bubble sort algorithm:
    taken from website:
        https://www.geeksforgeeks.org/python-program-to-sort-a-list-of-tuples-by-second-item/
    """
    list_to_sort = popularity_per_title()

    # getting length of list of tuples
    lst = len(list_to_sort)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (list_to_sort[j][1] > list_to_sort[j + 1][1]):
                temp = list_to_sort[j]
                list_to_sort[j] = list_to_sort[j + 1]
                list_to_sort[j + 1] = temp
    """
        for i in range(len(list_to_sort)):
        print(list_to_sort[i])
    """
    return list_to_sort

def get_days_since_purchase(database, ISBN_list):
    """
    sum days since purchase between all copies of a given book and get an average from today

    why average? some book copies may be bought at different dates.
    """
    date_format = "%d/%m/%Y"
    todays_date = date.today().strftime(date_format)
    avg_days_since_purchases = []

    for book in range(len(ISBN_list)):
        # print("ISBN: " + str(ISBN_list[book]))
        sum_days_per_book = 0
        copies_found = 0

        for entries in range(len(database)):
            if ISBN_list[book] == database[entries][CONST_ISBN_index]:
                copies_found = copies_found + 1
                purchase_date = database[entries][CONST_date_index]

                today = datetime.strptime(todays_date, date_format)
                purchase = datetime.strptime(purchase_date, date_format)

                delta = today - purchase     # gets the number of days since purchasing
                # print("days since purchase: " + str(delta.days) + ", purchase date: " + str(purchase_date)) # days since purchase, purchase date

                days_to_add = delta.days
                sum_days_per_book = days_to_add + sum_days_per_book

        # print(str(ISBN_list[book]) + " has " + str(sum_days_per_book))
        avg_days_since_purchases.append(sum_days_per_book/copies_found)

        # print(avg_days_since_purchases)

    return avg_days_since_purchases

def get_list_titles(database):
    """
    :parameter: database containing all books within, passed in as a list
    :return: list of all book titles, with respective copy counts

    This subroutine makes a list containing each book ISBN - each ISBN will only appear once;
    ISBN is used as ISBNs are unique for each book title.
    Some books will have the same title despite not being the same book
    """
    CONST_ISBN_index = 1

    ISBN_list = []

    for books in range(len(database)):
        if database[books][CONST_ISBN_index] not in ISBN_list:
            ISBN_list.append(database[books][CONST_ISBN_index])

    return ISBN_list
