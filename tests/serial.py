import pickle

entry = [x**2 for x in range(1,10)]
with open('entry.pickle', 'wb') as f:
    pickle.dump(entry, f) 
