from src.app.cli import cli

if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        raise e