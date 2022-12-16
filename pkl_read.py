import pickle

F=open(r'custom_universe.pkl','rb')

content=pickle.load(F)

print(content)