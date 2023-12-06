import json
import mysql.connector as mc
from sklearn.linear_model import LogisticRegression
import utils as u
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, ConfusionMatrixDisplay
import numpy as np

with open('creds.json') as file:
    creds = json.load(file)

query = '''
select * from elo where is_regular = 1
'''

data = u.sqlTodf(query, creds)
data['totalPoints'] = data['hpoints'] + data['vpoints']
data['hperc'] = data['hpoints'] / data['totalPoints']
data['vperc'] = data['vpoints'] / data['totalPoints']

n = len(data.index)
trainPerc = 0.95
trainSize = int(n * trainPerc)
train = data.iloc[:trainSize]
test = data.iloc[trainSize:]

features = ['home_elo', 'visitor_elo', 'home_per', 'visitor_per', 'hperc', 'vperc']
label = ['home_victory']

trainX, trainY = np.array(train[features]), np.array(train[label]).reshape(-1)
testX, testY = np.array(test[features]), np.array(test[label]).reshape(-1)

model = LogisticRegression(solver='liblinear')

model.fit(trainX, trainY)

prediction = model.predict(testX)

print("Accuracy:", accuracy_score(testY, prediction))
# print("Classification Report:\n", classification_report(testY, prediction))

# cm = confusion_matrix(testY, prediction)

# disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
# disp.plot(cmap='Blues', values_format='d')
# plt.title('Confusion Matrix for Logistic Regression Model')
# plt.show()