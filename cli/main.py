
try:
    import money_tracker
except ModuleNotFoundError:
    import sys, os
    sys.path.append(os.getcwd()) 
    import money_tracker

import typer
import accounts

app = typer.Typer()
app.add_typer(accounts.app, name="accounts")

if __name__ == "__main__":
    app()