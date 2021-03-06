from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    r = open(filename)
    soup = BeautifulSoup(r, 'html.parser')
    r.close()
    ans = []
    list1 = soup.find_all('tr', itemtype="http://schema.org/Book")
    for i in list1:
        added = (i.find('a', class_="bookTitle").text.strip(), i.find('a', class_="authorName").text.strip())
        ans.append(added)

    return ans
    


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    list1 = soup.find_all('a', class_="bookTitle")
    ans = []
    for i in range(0,10):
        ans.append("https://www.goodreads.com" + list1[i].get('href', None))
    return ans



def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    url = book_url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    name = soup.find('h1', id="bookTitle").text.rstrip()
    name = name[7:]
    aut = soup.find('a', class_="authorName").text.rstrip()
    page = soup.find('span', itemprop="numberOfPages").text.rstrip()
    page = int(page[:-6])
    return (name, aut, page)


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    fp = filepath
    r = open(fp)
    soup = BeautifulSoup(r.read(), 'html.parser')
    r.close()
    ans = []
    list1 = soup.find_all('div', class_="category clearFix")
    for i in list1:
        link = i.find('a')
        cat = link.text
        cat = cat[1:-5]
        url = link.get('href', None)
        tit = i.find('img', class_="category__winnerImage").get('alt', None)
        ans.append((cat, tit, url))
    return ans



def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w', newline='') as file:
        filewrite = csv.writer(file)
        filewrite.writerow(["Book Title", "Author Name"])
        for i in data:
            filewrite.writerow(i)


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    fp = filepath
    r = open(fp)
    soup = BeautifulSoup(r.read(), 'html.parser')
    r.close()
    ans = []
    text = soup.find('div', id="description").text

    fl2 = open("stopwords.txt")
    sw = fl2.readlines()
    fl2.close()
    sw1 = []
    for i in sw:
        word = i.rstrip()
        sw1.append(word[0].upper() + word[1:])

    reg = r'((\b[A-Z][a-zA-Z][a-zA-Z]+( [A-Z][a-zA-Z]+)+\b))'
    list1 = re.findall(reg, text)
    ans = []
    for i in list1:
        if len(i[0].split()) > 1 and i[0].split()[0] not in sw1:
            str1 = i[0]
            if str1[-1] == ' ':
                str1 = str1.rstrip()

            ans.append(str1)

    return ans

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls


    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        var = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(var), 20)
        # check that the variable you saved after calling the function is a list
        self.assertTrue(type(var) == list)
        # check that each item in the list is a tuple
        for i in var:
            self.assertTrue(type(i) == tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(var[0], ("Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(var[19], ("Harry Potter: The Prequel (Harry Potter, #0.5)", "J.K. Rowling"))

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        var = get_search_links()
        self.assertEqual(type(var), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(var), 10)
        
        # check that each URL in the TestCases.search_urls is a string
        for i in var:
            self.assertTrue(type(i), str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
            self.assertEqual(i[0:36], "https://www.goodreads.com/book/show/")     

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for i in get_search_links():
            summaries.append(get_book_summary(i))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
            # check that each item in the list is a tuple
        for j in summaries:
            self.assertEqual(type(j), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(j), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(j[0]), str)
            self.assertEqual(type(j[1]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(j[2]), int)
            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        var = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(var), 20)
            # assert each item in the list of best books is a tuple
        for i in var:
            self.assertEqual(type(i), tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(i), 3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(var[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(var[19], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        var = get_titles_from_search_results("search_results.htm")
        # call write csv on the variable you saved and 'test.csv'
        write_csv(var, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
        # check that there are 21 lines in the csv
        self.assertEqual(len(data), 21)
        # check that the header row is correct
        self.assertEqual(data[0], ["Book Title", "Author Name"])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(data[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(data[20], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])

    def test_extra_credit(self):
        self.assertEqual(len(extra_credit("extra_credit.htm")), 9)



if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



