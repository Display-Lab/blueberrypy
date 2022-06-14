import typer

from blueberrypy.services import _greeting

app = typer.Typer()


@app.command()
def greeting_cli(name: str = typer.Argument("world")):
    typer.echo(_greeting(name))
