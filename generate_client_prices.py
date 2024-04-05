import pandas as pd

# Client's product catalog (some overlap with books.toscrape.com)
client_products = {
    "A Light in the Attic": 55.00,
    "Tipping the Velvet": 50.00,
    "Soumission": 48.00,
    "Sharp Objects": 45.00,
    "Sapiens: A Brief History of Humankind": 52.00,
    "The Grand Design": 38.00,
    "The Martian": 42.00,
    "Fahrenheit 451": 30.00,
    "Dune": 35.00,
    "1984": 28.00
}

df = pd.DataFrame(list(client_products.items()), columns=["Product", "Client_Price"])
df.to_csv("client_prices.csv", index=False)
print("client_prices.csv created")
