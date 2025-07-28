
# # =========================BitHive===============================
# # ===   TEAM MEMBERS:                   =========================
# # ===   -> LAKSHYA PRAJAPATI            =========================
# # ===   -> REBANT PRATAP SINGH          =========================
# # ===   -> SATYAJIT SAHOO               =========================
# # ===============================================================



import joblib, os
from .pdf_parser import parse_spans
from .feature_extractor import extract_features
from src.utils.file_io import write_json
from langdetect import detect, DetectorFactory # Using langdetect
from langdetect.lang_detect_exception import LangDetectException


# Load the trained model and median_body font size
_data = joblib.load("models/heading_model.joblib")
_clf, _median_body = _data["model"], _data["median_body"]


# Set a seed for langdetect to ensure consistent results
# This is important because langdetect uses random sampling for short texts.
DetectorFactory.seed = 0 

# Helper to detect language of a given text using langdetect
def detect_language(text):
    if not text or len(text.strip()) < 5: # Increased minimum length for better accuracy
        return "unknown" # Default to unknown for very short texts
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"


def extract_outline_batch(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for f in os.listdir(input_dir):
        if f.lower().endswith(".pdf"):
            in_p = os.path.join(input_dir, f)
            spans = parse_spans(in_p)
            X = extract_features(spans, _median_body)
            preds = _clf.predict(X)

            # Store all predicted spans with their original data and predicted label
            predicted_spans_data = []
            for i, p in enumerate(preds):
                s = spans[i]
                predicted_spans_data.append({
                    "text": s["text"].strip(),
                    "page": s["page"],
                    "predicted_level": p,
                    "language": detect_language(s["text"].strip()) # Detect language here
                })
            
            title = os.path.basename(in_p) # Default title
            title_language = "unknown"
            
            combined_outline = []
            
            i = 0
            while i < len(predicted_spans_data):
                current_span_data = predicted_spans_data[i]
                level = current_span_data["predicted_level"]
                text = current_span_data["text"]
                page = current_span_data["page"]
                language = current_span_data["language"]

                if level == -1: # Process Title
                    combined_title_text = text
                    j = i + 1
                    # Combine all consecutive -1 spans on the same page
                    while j < len(predicted_spans_data) and \
                          predicted_spans_data[j]["predicted_level"] == -1 and \
                          predicted_spans_data[j]["page"] == page:
                        combined_title_text += " " + predicted_spans_data[j]["text"]
                        j += 1
                    title = combined_title_text.strip()
                    title_language = language # Language of the first title span or combined title
                    i = j # Move index past combined title spans
                    continue # Skip to next iteration, title is handled

                elif level > 0: # Process Headings (H1, H2, H3)
                    combined_heading_text = text
                    j = i + 1
                    # Combine consecutive spans if they have the same predicted level AND page
                    # Relaxing language check for combining headings to be more robust
                    while j < len(predicted_spans_data) and \
                          predicted_spans_data[j]["predicted_level"] == level and \
                          predicted_spans_data[j]["page"] == page:
                        combined_heading_text += " " + predicted_spans_data[j]["text"]
                        j += 1
                    
                    combined_outline.append({
                        "level": f"H{level}",
                        "text": combined_heading_text.strip(),
                        "page": page,
                        "language": language # Use the language of the first span in the combined heading
                    })
                    i = j # Move index past combined heading spans

                else: # Body text (level 0) or unclassified, skip for outline
                    i += 1
            
            # Construct the output JSON structure
            output_data = {
                "title": title,
                "title_language": title_language,
                "outline": combined_outline
            }

            # Save the JSON output
            write_json(output_data, os.path.join(output_dir, f[:-4]+".json"))

# # =========================BitHive===============================
# # ===   TEAM MEMBERS:                   =========================
# # ===   -> LAKSHYA PRAJAPATI            =========================
# # ===   -> REBANT PRATAP SINGH          =========================
# # ===   -> SATYAJIT SAHOO               =========================
# # ===============================================================