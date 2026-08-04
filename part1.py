from pprint import pprint

messages = [
{"user_id": "u1", "channel": "email", "message": "Hello, I want info about grants for education."},
{"user_id": "u2", "channel": "whatsapp", "message": " "},
{"user_id": "", "channel": "email", "message": "What is the deadline?"},
{"user_id": "u3", "channel": "email", "message": "Please send the report again."},
{"user_id": "u1", "channel": "whatsapp", "message": " Can you help me find funding? "},
{"user_id": "u4", "channel": "telegram", "message": "Good morning!"},
{"user_id": "u5", "channel": "email", "message": "Can you send me the scholarship document?"},
{"user_id": "u6", "channel": "whatsapp", "message": ""},
]

# i decided to use a list of categories and keywords in an order that seems to make sense 
# basing it on the priorities of the messaage and having the category "unknown" as a default.

category_keywords = [
    {"category": "grant_search", 
        "keywords": ["grant", "funding", "deadline", "scholarship"]},
    {"category": "report_request",
        "keywords": ["report", "file", "send again", "document"]},
    {"category": "general_questions",
        "keywords": ["how", "what", "can you", "where", "why"]},
]

def clean_and_classify(messages):
    cleaned_messages = []

    for msg in messages:
        clean_text = msg["message"].strip()

        if not msg["user_id"] or not clean_text:
            continue

        category = "unknown"
        search_text = clean_text.lower()

        for rule in category_keywords:
            if any(keyword in search_text for keyword in rule["keywords"]):
                category = rule["category"]
                break

        cleaned_msg = msg.copy()
        cleaned_msg["message"] = clean_text
        cleaned_msg["category"] = category

        cleaned_messages.append(cleaned_msg)

    return cleaned_messages

result = clean_and_classify(messages)

pprint(result)

'''
output:
[{'category': 'grant_search',
  'channel': 'email',
  'message': 'Hello, I want info about grants for education.',
  'user_id': 'u1'},
 {'category': 'report_request',
  'channel': 'email',
  'message': 'Please send the report again.',
  'user_id': 'u3'},
 {'category': 'grant_search',
  'channel': 'whatsapp',
  'message': 'Can you help me find funding?',
  'user_id': 'u1'},
 {'category': 'unknown',
  'channel': 'telegram',
  'message': 'Good morning!',
  'user_id': 'u4'},
 {'category': 'grant_search',
  'channel': 'email',
  'message': 'Can you send me the scholarship document?',
  'user_id': 'u5'}]
'''
