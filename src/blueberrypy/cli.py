import typer

from blueberrypy.services import _greeting

app = typer.Typer()

print("outside")

@app.command("hello")
def greeting_cli(name: str = typer.Argument("world")):
    print("inside")
    typer.echo(_greeting(name))

@app.command("goodbye")
def so_long():
    typer.echo("goodbye")

