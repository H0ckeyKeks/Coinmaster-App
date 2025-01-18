# Coinmaster App #
by Jasmin S.

#### Description: ####
The Coinmaster App offers two kinds of services: The user can either convert currency into another currency (for example USD in EUR) or the user can calculate the amount of bills and coins that are needed to pay for an amount that was given by the user.


### Download & Installation ###
1. Download the Repository through Clone Repository or Download Zip

2. After download, go to cmd and navigate to the project folder directory.

3. Use pip to install needed libraries.


### Usage: ###
Run the program python script app.py with python or you can run it by using flask run.


### Technologies used: ###
I used Python, Flask, HTML and CSS


### API used: ###
I used Frankfurter, an open-source API for currency exchange rates that is based on data sets published by the European Central Bank in Frankfurt/Germany. It provides current and historical exchange rates. The current exchange rates are updated daily around 16:00 CET.
You can find the API here: https://frankfurter.dev/


### Please note: ###
To make sure the program works properly, use pip to install needed libraries:

$ pip install -r requirements.txt


### About the project: ###

In a file called app.py created a directory called "countries" first which consists of the keys "country" and "denominations", as you can see here:

[directory](../../../source/repos/Coinmaster-App/grafik.png)

I then created various templates: index.html, breakdown.html, conversion.html and error.html

For each html template I created a function that handles the various cases that are linked to each html template.

Each function has both methods ('GET' and 'POST') as each function needs to send data to the server (the url) [-> GET] and in the request body (a form) [-> POST].

The index page of the Coinmaster App consists of a dropdown menu where the user can select a country. After that the user can choose wether to convert the selected currency to another currency or to breakdown an amount of money. The user can choose and click on the respective button. Each button will direct the user to the respective page (conversion / breakdown). On each page the user will be shown which country (and therefore currency) was selected and is asked to fill in the amount and - if the user chose the convert option - is asked to select the target currency from a dropdown menu. By clicking the button (convert / breakdown) the user starts the process and is given an answer by the Coinmaster App.
Each page has a button called home which will transfer the user back to the index page.

If there happens to be an error the Coinmaser App will transfer the user to an error message which explains what went wrong.

Examples for error messages:

- Amount must be a positive number
- Target currency not found
- Error fetching conversion rates

I made sure to handle as many errors as possible.


### Frontend: ###
I decided to create a styles.css file for the design of the Coinmaster App. I kept the colors neutral and went with a more modern output. Each page of the Coinmaster App looks the same so the user will know that this is still the Coinmaster App even when the user went from index to conversion / breakdown. The backround is a light blue while the content area is white. For the textcolor I chose 'dark charcoal' which is easy to read and a contrast to the light background colors. The titles are in a darker shade of blue which fits the overall pattern. The buttonns are the same color as the titles. The text on the buttons is white for better reading purposes. I decided to have everything centered, so the whole Coinmaster App catches the eye and looks well-ordered. There is not much going on in this app for accessibility reasons. It makes it easier for people to use a screenreader app.

I made sure that the Coinmaster App even works on smaller screens and mobile devices.

The footing consists of a small text stating the name of the App and the fact that it is a CS50 final project. I also added my name to show who created this program.
