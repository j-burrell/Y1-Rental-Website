from flask import Flask, render_template, request
import csv
import datetime

app = Flask(__name__)

@app.route("/")
def home():

    return render_template("home.html")

@app.route('/rental')
def rental():

    rentals = readFile('static\\userrentals.csv')
    date = currentDate()
    return render_template("rental.html", rentals = rentals, date=date)

@app.route('/attractions')
def attractions():
    return render_template('attractions.html')


@app.route('/review')
def review():

    reviewsFile = 'static\\reviews.csv'
    reviewsList = readFile(reviewsFile)

    return render_template('review.html', reviewsList=reviewsList)

#Function used to add reviews.
@app.route('/addReview', methods=['POST'])
def addReview():

    #File directory
    reviewsFile = 'static\\reviews.csv'

    #Gets details from html form.
    name = request.form['name']
    comment = request.form['comment']
    date = request.form['date']

    # Format into list for writing to file.
    date = dateFormatter(date)

    reviewEntry = [name, comment, date]

    # Check to see if all form entries have been filled.
    if (name == "" or comment == "" or date == ""):

        reviewList = readFile(reviewsFile)
        return render_template("review.html", reviewsList=reviewList)

    else:

        reviewsList = readFile(reviewsFile)
        reviewsList.append(reviewEntry)
        writeFile(reviewsList, reviewsFile)

        return render_template("review.html", reviewsList=reviewsList)


#Function used to add bookings.
@app.route('/addBooking', methods=['POST'])
def addBooking():

    #Returns the details inputted by the user on the html forms.
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']

    arrivalDate = request.form['arrivalDate']
    departureDate = request.form['departureDate']

    #Pass html dates into to change into easier to read date.
    arrivalDate = dateFormatter(arrivalDate)
    departureDate = dateFormatter(departureDate)

    approved = "No"

    #Format into list for writing to file.
    adminRental = [firstName, lastName, arrivalDate, departureDate, email, approved]
    userRental = [arrivalDate, departureDate, approved]

    #File directories for csvs.
    adminCSV = 'static\\adminrentals.csv'
    userCSV = 'static\\userrentals.csv'

    #Check to see if all form entries have been filled.
    if (firstName == "" or lastName == "" or email == "" or arrivalDate == "" or departureDate == ""):

        rentals = readFile(userCSV)
        return render_template("rental.html", rentals=rentals)

    else:

        rentals = readFile(adminCSV)
        rentals.append(adminRental)
        writeFile(rentals, adminCSV)

        rentals = readFile(userCSV)
        rentals.append(userRental)
        writeFile(rentals, userCSV)

        return render_template("rental.html", rentals=rentals)

#Reads csv files for outputting into html.
def readFile(fileName):
    with open(fileName, 'r') as inFile:
        reader = csv.reader(inFile)
        rentals = [row for row in reader]
    return rentals

#Writes rows of lists into a csv file.
def writeFile(rentals, fileName):
    with open(fileName, 'w', newline="") as outFile:
        writer = csv.writer(outFile)
        writer.writerows(rentals)
    return

#Formats dates into day/month/year instead of year-month-day that html returns.
def dateFormatter(date):

    dateSeperated = date.split("-")
    dateSeperated.reverse()
    formatedDate = '/'.join(dateSeperated)

    return formatedDate

#Returns current date.
def currentDate():

    date = datetime.datetime.today().strftime('%Y-%m-%d')
    return date

if __name__ == "__main__":
    app.run(debug=True)
