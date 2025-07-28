

# =========================BitHive===============================
# ===   TEAM MEMBERS:                   =========================
# ===   -> LAKSHYA PRAJAPATI            =========================
# ===   -> REBANT PRATAP SINGH          =========================
# ===   -> SATYAJIT SAHOO               =========================
# ===============================================================



import click
import src.train_model as tm
from src.round1a.heading_detector import extract_outline_batch

# Define the Path types separately for clarity
INPUT_PATH_TYPE = click.Path(exists=True, file_okay=False, dir_okay=True)
OUTPUT_PATH_TYPE = click.Path(file_okay=False, dir_okay=True)

@click.command()
@click.option("--round", "rng", required=True, type=click.Choice(["train","1A"]),
              help="Specify the round to run: 'train' for model training, '1A' for PDF outline extraction.")
# Corrected: Removed 'help' argument from @click.argument
@click.argument("input_dir", type=INPUT_PATH_TYPE)
# Corrected: Removed 'help' argument from @click.argument
@click.argument("output_dir", type=OUTPUT_PATH_TYPE)
def main(rng, input_dir, output_dir):
    """
    Main entry point for the Adobe India Hackathon solution.

    INPUT_DIR: Path to the input directory containing PDF files.
    OUTPUT_DIR: Path to the output directory for JSON results.

    This script handles model training or PDF outline extraction based on the
    --round option.
    """
    if rng=="train":
        print("Starting model training...")
        tm.main()
        print("Model training completed.")
    else: # rng == "1A"
        print(f"Processing PDFs from '{input_dir}' and saving outlines to '{output_dir}'...")
        extract_outline_batch(input_dir, output_dir)
        print("PDF processing completed. Outlines generated.")

if __name__=="__main__":
    main()



# =========================BitHive===============================
# ===   TEAM MEMBERS:                   =========================
# ===   -> LAKSHYA PRAJAPATI            =========================
# ===   -> REBANT PRATAP SINGH          =========================
# ===   -> SATYAJIT SAHOO               =========================
# ===============================================================