import pickle


with open('../first-innings-score-lr-model.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data)