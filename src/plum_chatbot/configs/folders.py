from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"

LOGS_DIR = BASE_DIR / "logs"

if __name__ == "__main__":
    print(f"Base Directory: {BASE_DIR}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Logs Directory: {LOGS_DIR}")

    # Create directories if they do not exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
