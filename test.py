import pickle
colli0 = [[[0,500],[300,500]],[[800,400],[500,400]],[[500,450],[60,125],[1,1,400,650]]]
colli1 = [[[-20, 545], [343, 120], [0, 0, -100, -100]], [[160, 425], [320, 221], [0, 0, -100, -100]], [[267, 294], [213, 200], [0, 0, -100, -100]], [[477, -21], [210, 320], [1, 1, 477, 842]], [[457, 473], [573, 171], [0, 0, -100, -100]], [[410, 399], [68, 71], [1, 1, 410, 963]]]
pickle.dump(colli0, open("levels.pkl","wb"))
pickle.dump(colli1, open("levels.pkl","ab"))
