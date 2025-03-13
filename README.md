
# Run steps

## Install dependencies
`pip install mysql-connector-python`

## Create database (requires MySQL root privileges)
`mysql -u root -p < database/GROUP6.sql`

## Import sample data
`mysql -u root -p GROUP6 < database/sample_data.sql`

## Modify this configuration line
```
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",  # Change to your MySQL password
    database="GROUP6"
)
```

## Start program
`python src/main.py`