import typer
from typing import Optional
from pathlib import Path

app = typer.Typer()

@app.command()
def main(extension: str = typer.Argument(...,help="l'extensiion des fichiers à cherchés"),
        directory:Optional[str] = typer.Argument(None,help ="dossier dans lequel cherchés"),
        delete: bool = typer.Option(False,help="supprimés les fichiers trouvés") ):
    """affiche les fichiers trouvés avec l'extension donnée"""
    
    if directory:
        directory = Path(directory)  # type: ignore
    else:
        directory = Path.cwd()  # type: ignore
    
    if not directory.exists():  # type: ignore
        typer.secho(f"le dossier '{directory}' n'existe pas ",fg = typer.colors.RED)
        raise typer.Exit()
    files = directory.rglob(f"*.{extension}")  # type: ignore
    if delete:
        typer.confirm("Voulez-vous vraiment supprimer tous les fichiers trouvés ?", abort=True)
        for file in files:
            file.unlink()
            typer.secho(f"suppression du fichier {file}",fg=typer.colors.RED)
    else:
        typer.secho(f"Fichiers trouvés avec l'extension {extension}",fg=typer.colors.BRIGHT_WHITE,bg=typer.colors.BLUE)
        for file in files:
            typer.echo(file)

@app.command()
def search(extension:str):
    """chercher les fichiers avec l'extension donnée"""
    main(extension=extension,directory=None,delete=False)

@app.command()
def delete(extension:str):
    """supprimer les fichiers avec l'extension donnée"""
    main(extension=extension,directory=None,delete=True)


if __name__ == "__main__":
    app()
