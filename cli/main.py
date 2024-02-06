
try:
    import money_tracker
except ModuleNotFoundError:
    import sys, os
    sys.path.append(os.getcwd()) 
    import money_tracker

import typer
import accounts
import categories
import transactions

app = typer.Typer()
app.add_typer(accounts.app, name="accounts")
app.add_typer(categories.app, name="categories")
app.add_typer(transactions.app, name="transactions")

if __name__ == "__main__":
    app()