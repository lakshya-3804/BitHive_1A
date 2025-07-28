# SmartPDF: Connecting the Dots - Round 1A: Understand Your Document

This repository contains the solution for Round 1A of the Adobe India Hackathon's "Connecting the Dots" challenge, focusing on extracting structured outlines from PDF documents.

## Table of Contents

1.  [Challenge Overview](#1-challenge-overview)
2.  [Features](#2-features)
3.  [Project Structure](#3-project-structure)
4.  [Setup & Installation](#4-setup--installation)
    * [Prerequisites](#prerequisites)
    * [Local Setup](#local-setup)
5.  [Usage](#5-usage)
    * [Training the Model](#training-the-model)
    * [Running Inference](#running-inference)
6.  [Dockerization](#6-dockerization)
    * [Building Docker Image](#building-docker-image)
    * [Running Docker Container](#running-docker-container)
7.  [Methodology & Approach Explanation](#7-methodology--approach-explanation)
8.  [Constraints Adherence](#8-constraints-adherence)
9.  [Future Improvements](#9-future-improvements)

---

## 1. Challenge Overview

**Round 1A: Understand Your Document:** The mission is to extract a structured, hierarchical outline (Title, H1, H2, H3) from raw PDF files. This outline serves as a foundational layer for smarter document experiences.

## 2. Features

* **PDF Parsing:** Extracts raw text spans, font sizes, and positional metadata from PDFs.
* **Structured Outline Extraction:** Identifies document titles and hierarchical headings (H1, H2, H3) using a custom-trained machine learning model.
* **Offline Execution:** All models and dependencies are designed to run without internet access during execution.
* **Dockerized Solution:** Provides a portable and reproducible environment.

## 3. Project Structure

This directory (`Challenge_1A`) contains the Round 1A solution.


```
Challenge_1A/  
├── data/  
│   ├── input_pdfs/               # Place your input PDFs here for processing  
│   ├── annotations_template.csv  # Generated template for manual labeling  
│   └── annotations.csv           # Manually labeled training data for R1A model  
├── models/  
│   └── heading_model.joblib      # Trained R1A heading detection model (output of training)  
├── output/                       # Output directory for generated JSON outlines  
├── scripts/  
│   └── export_spans.py           # Script to extract raw spans to create annotations_template.csv  
├── src/  
│   ├── init.py  
│   ├── main.py                   # R1A main entry point  
│   ├── round1a/                  # Core logic for R1A  
│   │   ├── init.py  
│   │   ├── feature_extractor.py  # Extracts numerical features from PDF spans  
│   │   ├── heading_detector.py   # Loads model and performs heading prediction  
│   │   └── pdf_parser.py         # Parses PDF content into text spans  
│   └── train_model.py            # R1A model training script  
├── venv/                         # Python virtual environment  
├── Dockerfile                    # Dockerfile for R1A solution  
└── requirements.txt              # Python dependencies for R1A  
```


## 4. Setup & Installation

### Prerequisites

* **Python 3.8+:** Ensure Python is installed on your system.
* **pip:** Python package installer (usually comes with Python).
* **Docker Desktop:** Required for building and running Docker containers. Make sure it's installed and running, and that your user has permissions to run Docker commands.

### Local Setup

1.  **Navigate to the `Challenge_1A` directory:**
    ```bash
    cd Challenge_1A
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # For PowerShell:
    .\venv\Scripts\Activate.ps1
    # For Command Prompt:
    venv\Scripts\activate
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install numpy
    pip install -r requirements.txt
    ```

## 5. Usage

(Ensure you are in the `Challenge_1A` directory and your virtual environment is active)

### Training the Model

This step creates the `models/heading_model.joblib` file based on your labeled data.

1.  **Place sample PDFs** in `data/input_pdfs/` that you want to use for training.
2.  **Generate annotation template:**
    ```bash
    python scripts/export_spans.py
    ```
    This creates `data/annotations_template.csv`.
3.  **Manually label `annotations_template.csv`:** Open this CSV file in a spreadsheet editor (like Excel, Google Sheets, LibreOffice Calc). For each row (text span), manually fill in the `label` column with:
    * `-1` for the document title.
    * `0` for normal body text.
    * `1` for H1 headings.
    * `2` for H2 headings.
    * `3` for H3 headings.
    * **Save this finalized file as `data/annotations.csv`**.
4.  **Train the model:**
    ```bash
    python -m src.main --round train data/input_pdfs output/
    ```
    This command executes the `train_model.py` script, which reads your `annotations.csv` and creates the `heading_model.joblib` file.

### Running Inference

This uses the trained model to extract outlines from new PDFs.

1.  **Place PDFs to analyze** in `data/input_pdfs/`.
2.  **Run the analysis:**
    ```bash
    python -m src.main --round 1A data/input_pdfs output/
    ```
    Output JSONs (e.g., `your_pdf_name.json`) will be saved in `output/`.

## 6. Dockerization

Docker provides a consistent and isolated environment for building and running the solution.

### Building Docker Image

(Ensure you are in the `Challenge_1A` directory)

1.  **Ensure `Dockerfile` is present** in the `Challenge_1A` directory with the following content:
    ```dockerfile
    # Use a lightweight Python base image that is compatible with AMD64 architecture.
    FROM --platform=linux/amd64 python:3.10-slim-buster

    # Set the working directory inside the container
    WORKDIR /app

    # Copy the requirements file and install dependencies
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # Copy the trained model from your local 'models' directory
    COPY models/heading_model.joblib /app/models/heading_model.joblib

    # Copy the rest of the application code
    COPY . .

    # The command to run your solution for Round 1A.
    # The `docker run` command will mount the input/output directories.
    CMD ["python", "-m", "src.main", "--round", "1A", "/app/input", "/app/output"]
    ```
2.  **Build the Docker image:**
    ```bash
    docker build --platform linux/amd64 -t mysolution_r1a:latest .
    ```
    *(Note: The first build might take significant time due to base image download and dependency installation.)*

### Running Docker Container

(Ensure you are in the `Challenge_1A` directory)

* **For PowerShell or Git Bash:**
    ```bash
    docker run --rm -v "$(pwd)/data/input_pdfs":/app/input -v "$(pwd)/output":/app/output --network none mysolution_r1a:latest
    ```
* **For Command Prompt (CMD):**
    ```cmd
    docker run --rm -v "%cd%\data\input_pdfs":/app/input -v "%cd%\output":/app/output --network none mysolution_r1a:latest
    ```

## 7. Methodology & Approach Explanation

The core idea is to classify each text segment (span) in a PDF as a specific heading level (H1, H2, H3), a title, or body text.

1.  **PDF Parsing:** Utilizes `PyMuPDF` (`fitz`) to extract text at a granular level, treating each contiguous run of text with consistent formatting as a "span." This provides not just text, but also crucial metadata like font size, position (x0, y0), and font flags (e.g., bold).
2.  **Feature Engineering:** For each extracted span, a numerical feature vector is generated. Key features include:
    * **Absolute Font Size:** The raw font size of the text.
    * **Bold Flag:** A binary indicator if the text is bold.
    * **Word Count:** Number of words in the span.
    * **Uppercase Ratio:** Proportion of uppercase characters (helps identify ALL CAPS headings).
    * **Numerical Prefix:** A flag if the text starts with a common numbering pattern (e.g., "1.1").
    * **Relative Font Size:** The most powerful feature, calculated as `span_font_size / median_body_font_size`. This normalizes font sizes across documents, as headings are typically larger than the main body text. The `median_body_font_size` is calculated from manually labeled body text during training.
3.  **Classification:** A `RandomForestClassifier` is trained on these features using a manually labeled dataset (`annotations.csv`). The model learns to map feature patterns to heading levels.
4.  **Outline Construction:** During inference, the trained model predicts the label for each span. Consecutive spans predicted as the same heading level on the same page are intelligently combined into a single entry for a cleaner, more readable outline. The document title is identified by a specific label (`-1`).

## 8. Constraints Adherence

* **CPU Only:** All models (PyMuPDF, scikit-learn) are configured to run on CPU.
* **Model Size ≤ 200MB:** The `joblib` file for the custom classifier is very small (KBs), well within the limit.
* **Processing Time ≤ 10 seconds (for 50-page PDF):** The chosen models and efficient parsing/feature extraction are designed for fast processing. The `slim-buster` Docker image and optimized `pip install` ensure a lean environment.
* **No Internet Access during Execution:** All necessary models are pre-trained and copied into the Docker image. The `docker run` commands explicitly use `--network none`.

## 9. Future Improvements

* **More Diverse Training Data:** Expanding the `annotations.csv` with more examples from various PDF layouts would improve generalization.
* **Advanced Layout Features:** Incorporating features like indentation, spacing between lines/blocks, and line-height ratios could further enhance accuracy.
* **Error Handling:** More robust error handling within PDF parsing for malformed documents.
