# SmartPDF: Connecting the Dots - Round 1A: Understand Your Document

## 💡 Rethink Reading. Rediscover Knowledge.

This repository contains the solution for **Round 1A: Understand Your Document** of the Adobe India Hackathon's "Connecting the Dots" challenge. Our mission is to transform static PDFs into intelligent, structured outlines, making them machine-readable and paving the way for smarter document experiences.

---

## 🚀 Features

* **PDF Parsing Powerhouse:** Leverages `PyMuPDF` for robust and efficient extraction of every text span, including content, precise font sizes, positional data, and crucial font flags (bold, italic).
* **Intelligent Outline Extraction:** Employs a custom-trained `RandomForestClassifier` to accurately identify document titles and hierarchical headings (H1, H2, H3).
* **Seamless Aggregation:** Implements a sophisticated post-processing step to combine continuous text spans belonging to the same predicted heading level (or title) on the same page. This ensures a clean, cohesive, and highly readable output outline.
* **Multilingual Support:** Automatically detects the language of the document title and each extracted heading using the `langdetect` library, adding valuable linguistic metadata for global document understanding.
* **Offline First:** Designed for complete offline execution, ensuring high performance and adherence to hackathon constraints.
* **Dockerized for Portability:** Comes with a meticulously crafted `Dockerfile` to provide a consistent, reproducible, and self-contained environment for effortless building and deployment.

---

## 🛠️ Tech Stack Used

* **Python 3.10:** The backbone of our solution.
* **PyMuPDF (fitz):** For lightning-fast PDF text and metadata extraction.
* **scikit-learn:** Our choice for robust machine learning model training and inference.
* **NumPy & Pandas:** Essential for efficient numerical computations and data manipulation.
* **Joblib:** For streamlined serialization and deserialization of our trained models.
* **Click:** Powers our user-friendly command-line interface.
* **langdetect:** Our go-to for accurate multilingual language identification.
* **Docker:** For seamless containerization and environment consistency.

---

## 📂 Project Structure

Our modular project design keeps Round 1A self-contained for clarity and ease of use.





Challenge_1A/
├── data/
│   ├── input_pdfs/               # 📥 Your PDFs for processing/training go here
│   ├── annotations_template.csv  # 📝 Generated template for manual labeling (Step 1 of training)
│   └── annotations.csv           # 📊 Your custom, manually labeled training dataset for R1A model
├── models/
│   └── heading_model.joblib      # 🧠 Trained R1A heading detection model (Output of training)
├── output/                       # 📄 Directory for generated JSON outlines
├── scripts/
│   └── export_spans.py           # 🚀 Script to extract raw spans from PDFs (for annotations_template.csv)
├── src/
│   ├── init.py               # Python package marker
│   ├── main.py                   # 🏁 Main entry point for running R1A (training or inference)
│   ├── round1a/                  # Core logic for Round 1A
│   │   ├── init.py           # Python package marker
│   │   ├── feature_extractor.py  # Extracts numerical features from PDF spans
│   │   ├── heading_detector.py   # Loads model, predicts, aggregates, and adds language detection
│   │   └── pdf_parser.py         # Parses PDF content into text spans
│   └── train_model.py            # 🚂 R1A model training script
├── venv/                         # Python virtual environment (recommended for local development)
├── Dockerfile                    # 🐳 Dockerfile for building the R1A solution container
└── requirements.txt              # Python dependencies for R1A




---

## 📈 Flow Diagram and Working Explanation

### Flow Diagram

```mermaid
graph TD
    A[Start] --> B{PDF Document};
    B --> C[PDF Parser (pdf_parser.py)];
    C --> D{Text Spans + Metadata};
    D --> E[Feature Extractor (feature_extractor.py)];
    E --> F{Numerical Features};
    F --> G[Trained Model (heading_model.joblib)];
    G --> H{Predicted Labels (Title, H1, H2, H3, Body)};
    H --> I[Heading Detector (heading_detector.py)];
    I --> J{Aggregation Logic};
    J --> K{Language Detector (langdetect)};
    K --> L{Combined Headings + Language};
    L --> M[Output JSON];
    M --> N[End];

    subgraph Training Flow
        O[Start Training] --> P{Input PDFs};
        P --> Q[Export Spans (export_spans.py)];
        Q --> R{Raw Spans CSV (annotations_template.csv)};
        R --> S[Manual Labeling];
        S --> T{Labeled Dataset (annotations.csv)};
        T --> U[Train Model (train_model.py)];
        U --> V{Trained Model (heading_model.joblib)};
        V --> W[End Training];
    end