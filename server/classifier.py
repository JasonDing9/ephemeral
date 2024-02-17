import torch
import torch.nn as nn
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer
from actions import create_email

CLASSES = ["clarify", "email", "link", "schedule", "todos", "unknown"]

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
    input_ = torch.Tensor(encoder.encode([text]))
    output = classifier(input_)
    action = CLASSES[output.argmax(1)]
    print(action)
    if action == 'email':
        create_email(text)

# classify("Parth said: I will send an email to Arvind to remind him to finish the project by this Friday.")