import sys
import os
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from src.predict import NewsPredictor

def run_test():
    print("Loading reusable prediction module...")
    predictor = NewsPredictor()
    print("Models loaded. Running samples...\n")
    
    samples = [
        {
            "title": "Donald Trump Sends Out Embarrassing New Year’s",
            "text": "Donald Trump just couldn t wish all Americans a happy new year..."
        },
        {
            "title": "Republican House Speaker Ryan backs Trump after long courtship",
            "text": "WASHINGTON (Reuters) - Paul Ryan, the top elected Republican, ended a long period of soul-searching and endorsed Donald Trump for president on Thursday..."
        },
        {
            "title": "ALIENS LAND IN CENTRAL PARK",
            "text": "Extraterrestrials have taken over New York and demand our pizza. The mayor has surrendered."
        }
    ]
    
    for i, s in enumerate(samples, 1):
        print(f"--- Sample {i} ---")
        print(f"Title: {s['title']}")
        res = predictor.predict(s['title'], s['text'])
        print("Prediction Result:")
        print(json.dumps(res, indent=2))
        print()

if __name__ == '__main__':
    run_test()
