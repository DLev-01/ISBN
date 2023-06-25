from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form/ISBN-10')
def form1():
    return render_template('form1.html')

@app.route('/form/ISBN-13')
def form2():
    return render_template('form2.html')

@app.route('/processed', methods=['post'])
def processing_mod11():
    book_data = {
        "title": request.form['b_title'],
        "ISBN": request.form['b_isbn'],
    }
    def is_valid_isbn_10(isbn):
        checksum = sum(int(digit) * (10 - index) for index, digit in enumerate(isbn[:-1]))
        if (checksum + (10 if isbn[-1] == 'X' else int(isbn[-1]))) % 11 != 0:
            return False
        return True
    try:
        int(book_data['ISBN'])
        if len(book_data['ISBN']) != 10:
            return render_template('error.html')
        else:
            isbn = book_data['ISBN']
            if is_valid_isbn_10(isbn) == True:
                return render_template ('results_isbn10V.html', book_data = book_data)
            else:
                return render_template ('results_isbn10F.html', book_data = book_data)
    except:
        return render_template ('error.html')

@app.route('/processed#', methods=['post'])
def processing_mod10():
    book_data = {
        "title": request.form['b_title'],
        "ISBN": request.form['b_isbn'],
    }
    def is_valid_isbn_13(isbn):
        checksum = sum(int(digit) * (3 if index % 2 == 0 else 1) for index, digit in enumerate(isbn[:-1]))
        check_digit = (10 - (checksum % 10)) % 10
        if int(isbn[-1]) != check_digit:
            return False
        return True
    try:
        int(book_data['ISBN'])
        if len(book_data['ISBN']) != 13:
            return render_template('error.html')
        else:
            isbn = book_data['ISBN']
            if is_valid_isbn_13(isbn) == True:
                return render_template ('results_isbn13V.html', book_data = book_data)
            else:
                return render_template ('results_isbn13F.html', book_data = book_data)
    except:
        return render_template ('error.html')

if __name__ == "__main__":
    app.run(debug=True)