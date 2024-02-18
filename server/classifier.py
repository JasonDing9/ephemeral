import torch
import torch.nn as nn
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer
from actions.get_link import get_link
from actions.schedule_event import create_event

from actions.create_email import create_email
from actions.clarify_search import clarify_search
from actions.assistant import assistant
from actions.imageGen import create_summary_image

CLASSES = ["clarify", "email", "link", "schedule", "unknown"]

class ActionClassifier(torch.nn.Module):
    def __init__(self):
        super(ActionClassifier, self).__init__()
        self.fc1 = nn.Linear(768, 384)
        self.dropout1 = nn.Dropout(0.2)
        self.fc2 = nn.Linear(384, 384)
        self.dropout2 = nn.Dropout(0.2)
        self.fc3 = nn.Linear(384, 384)
        self.dropout3 = nn.Dropout(0.2)
        self.fc4 = nn.Linear(384, 384)
        self.dropout4 = nn.Dropout(0.2)
        self.fc5 = nn.Linear(384, len(CLASSES))
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = F.gelu(self.fc1(x))
        x = self.dropout1(x)
        x = F.gelu(self.fc2(x))
        x = self.dropout2(x)
        x = F.gelu(self.fc3(x))
        x = self.dropout3(x)
        x = F.gelu(self.fc4(x))
        x = self.dropout4(x)
        x = F.gelu(self.fc5(x))
        x = self.softmax(x)
        return x

encoder = SentenceTransformer('all-mpnet-base-v2')
classifier = ActionClassifier()
classifier.load_state_dict(torch.load("action_classifier.pt"))

def classify(text):
    if 'assistant' in text.lower():
        print("Classified as assistant.")
        return assistant(text)
    elif 'send' in text.lower() and 'email' in text.lower():
        print("Classified as email.")
        return create_email(text)
    elif 'write' in text.lower() and 'email' in text.lower():
        print("Classified as email.")
        return create_email(text)
    elif 'schedule' in text.lower():
        print("Classified as schedule.")
        return create_event(text)
    elif 'set' in text.lower() and 'up' in text.lower() and 'meeting' in text.lower():
        print("Classified as schedule.")
        return create_event(text)
    elif 'open up' in text.lower():
        print("Classified as link.")
        return get_link(text)
    elif 'cheers' in text.lower():
        print("Classified as meeting over.")
        create_summary_image()
        return None
    
    input_ = torch.Tensor(encoder.encode([text]))
    output = classifier(input_)
    action = CLASSES[output.argmax(1)]
    print("Classified as: " + action)
    
    if action == 'email':
        return create_email(text)
    elif action == 'clarify':
        return clarify_search(text)
    elif action == 'schedule':
        return None
        # return create_event(text)
    elif action == 'link':
        return get_link(text)