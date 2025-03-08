from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load your fine-tuned BERT model (placeholder paths)
MODEL_PATH = "fine_tuned_model"
TOKENIZER_PATH = "fine_tuned_model"

# Load the model
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)

def predict_job_title(text):
    try:
        # Create input text
        input_text = text
        
        # Tokenize input
        inputs = tokenizer(
            input_text,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )
        
        # Make prediction
        outputs = model(**inputs)
        predicted_class = torch.argmax(outputs.logits, dim=1).item()
        
        # Map class index to job title (update with your labels)
        job_titles = {
            0: "Python Developer",
            1: "Database Administrator",
            2: "Software Developer",
            3: "Network Administrator",
            4: "Project Manager",
            5: "Security Analyst",
            6: "Web Developer",
            7: "Systems Administrator",
            8: "Java Developer",
            9: "Front End Developer"
            # Add your actual job titles
        }
        
        return job_titles.get(predicted_class, "General Professional")
    
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")