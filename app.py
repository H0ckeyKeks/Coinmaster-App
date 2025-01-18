from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)

# Supported countries and denominations
countries = {
    "USA": {"currency": "USD", "denominations": [100, 50, 20, 10, 5, 2, 1, 0.25, 0.10, 0.05, 0.01]},
    "Germany": {"currency": "EUR", "denominations": [500, 200, 100, 50, 20, 10, 5, 1, 2, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01]},
    "UK": {"currency": "GBP", "denominations": [50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01]},
    "Canada": {"currency": "CAD", "denominations": [100, 50, 20, 10, 5, 2, 1, 0.50, 0.25, 0.10, 0.05]},
    "Sweden": {"currency": "SEK", "denominations": [1000, 500, 200, 100, 50, 20, 10, 5, 2, 1]},
    "Switzerland": {"currency": "CHF", "denominations": [1000, 200, 100, 50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05]},
    "Japan": {"currency": "JPY", "denominations": [10000, 5000, 2000, 1000, 500, 100, 50, 10, 5, 1]}
}

country_currency = ["USD", "EUR", "GBP", "CAD", "SEK", "CHF", "JPY"]


@app.route('/', methods=['GET', 'POST'])
# Function to run when someone accesses the / route of the app
def index():
    if request.method == 'GET':
        # Update index data with countries for the dropdown menu
        return render_template('index.html', countries=list(countries.keys()))

    if request.method == 'POST':
        # Save user input
        action = request.form.get('action')
        country = request.form.get('country')

        if not country:
            error_input = "Please select a country to proceed."
            return render_template('index.html', error_message=error_input, countries=list(countries.keys()))

        if action == 'conversion':
            # Go to conversion.html but keep the data that was provided by the user in index.html
            return redirect(url_for('.convert_currency', country=country))

        if action == 'breakdown':
            # Go to breakdown   .html but keep the data that was provided by the user in index.html
            return redirect(url_for('.calculate_breakdown', country=country))


@app.route('/conversion', methods=['GET', 'POST'])
# Function for conversion
def convert_currency():
    if request.method == 'GET':
        country = request.args.get('country')
        return render_template(
            'conversion.html', selected_country=country, selected_currency=countries.get(country, {}).get("currency"), target_country=list(country_currency))

    if request.method == 'POST':
        # Getting input from the form in the html template
        base_country = request.form.get('selected_country')
        base_currency = request.form.get('selected_currency')
        target_currency = request.form.get('target_country')
        # Convert amount from string to float for conversion in line 71
        amount = float(request.form.get('amount'))

    # Call API for exchange rates
    try:
        # Validate Input
        if not isinstance(amount, (int, float)) or amount <= 0:
            error_amount = "Amount must be a positive number"
            return render_template('error.html', error_message=error_amount), 400

        # Request to API an retrieving rate data
        response = requests.get("https://api.frankfurter.app/latest",
                                params={'base': base_currency, 'symbols': target_currency})

        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", ())

            # Handling errors / checking if target currency exists
            if target_currency not in rates:
                error_currency = f"Currency {target_currency} not found."
                return render_template('error.html', error_message=error_currency), 400

            # Conversion
            converted_amount = round((amount * rates[target_currency]), 2)
            # Updating the data of the template
            return render_template('conversion.html', conversion_result=converted_amount, amount=amount, selected_currency=base_currency, target_currency=target_currency, selected_country=base_country)
        else:
            # Handling API error
            if response.status_code != 200:  # Adjust condition to detect the error
                error_message = "Error fetching conversion rates"
                error_details = response.text  # Details from the failed response
            return render_template(
                'error.html',
                error_message=error_message,
                error_details=error_details
            ), response.status_code
    except Exception as e:
        # Catch unforseen errors
        return render_template(
            'error.html',
            error_message="An unexpected error occurred.",
            error_details=str(e)
        ), 500


@app.route('/breakdown', methods=['GET', 'POST'])
# Function for denomination
def calculate_breakdown():
    if request.method == 'GET':
        # Gets the country from URL
        country = request.args.get('country')
        return render_template('breakdown.html', selected_country=country, denominations=countries.get(country, {}).get('denominations'))

    if request.method == 'POST':
        selected_country = request.form.get('selected_country')
        amount = float(request.form.get('amount'))

        denominations = countries.get(selected_country, {}).get('denominations', [])
        if not denominations:
            error_denom = "Unsupported country."
            return render_template('error.html', error_message=error_denom), 400

        breakdown = {}
        for d in denominations:
            count, amount = divmod(amount, d)
            if count:
                breakdown[f"{d:.2f}"] = int(count)
                formatted_result = ', '.join(f"{v} x {k}" for k, v in breakdown.items())

        return render_template('breakdown.html', breakdown_result=formatted_result, amount=amount, selected_currency=selected_country)


if __name__ == '__main__':
    app.run(debug=True)
