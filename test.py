import pickle
data = []
with open('levels.pkl', 'rb') as fr:
    try:
        while True:
            data.append(pickle.load(fr))
    except EOFError:
        pass
print(data)