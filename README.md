# sqlmodel-generator
model code to generate sqlmodel from the database

## Usage

#### Edit the `generator.py` file

```
url = URL.create("postgresql+psycopg", database="your_database")
```

#### Run

```
python generator.py
python generator.py > models.py
```