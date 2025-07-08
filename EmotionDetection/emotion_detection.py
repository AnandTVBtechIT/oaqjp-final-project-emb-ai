import requests
import json

def emotion_detector(text_to_analyse):
    """
    Calls Watson NLP API to analyze the emotions in the given text.
    Returns a dictionary with emotion scores and dominant emotion.
    Returns all None on error/invalid input.
    """
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"Content-Type": "application/json",
               "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = json.dumps({"raw_document": {"text": text_to_analyse}})
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 400:
            return {'anger': None, 'disgust': None, 'fear': None,
                    'joy': None, 'sadness': None, 'dominant_emotion': None}
        response_json = response.json()
        emotions = response_json['emotionPredictions'][0]['emotion']
        dominant_emotion = max(emotions, key=emotions.get)
        return {
            'anger': emotions.get('anger'),
            'disgust': emotions.get('disgust'),
            'fear': emotions.get('fear'),
            'joy': emotions.get('joy'),
            'sadness': emotions.get('sadness'),
            'dominant_emotion': dominant_emotion
        }
    except Exception as e:
        # For any error, return all None
        return {'anger': None, 'disgust': None, 'fear': None,
                'joy': None, 'sadness': None, 'dominant_emotion': None}