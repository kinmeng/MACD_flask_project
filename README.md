# MACD_flask_project
 This project provides trading information to users based on the MACD indicator. The algorithm built provides value by matching the likely signals 'overbought' and 'oversold' to the appropriate MACD crossovers. A quick observation suggests that the results provided are accurate around 60% of the time, better than the stock screeners which does not match the appropriate signals to the right MACD crossovers

The deployed flask app is here: http://35.240.166.48:8080/results

How to download and run the files locally:

1. Download the files in .zip
2. Pip3 install all modules listed in requirements.txt (pip3 install -r requirements.txt)
3. Setup database with the credentials as stated in the connection string
4. Setup models in the database by running the following commands
-python3 manage.py db init
-python3 manage.py db migrate
-python3 manage.py db upgrade
5. Before starting to run, a kind reminder that this flask app is run on port 8080. If you wish to make changes, please do so in the manage.py app (by editing the Server function).
