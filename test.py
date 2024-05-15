import os


with open("saved beats/test.bmsf", "r") as file:
    data = file.read()
    data = data.split("\n")
    bpm = int(data[0])
    tones = data[1].strip().split(",")
    del tones[-1]
    tones = [tone.strip() for tone in tones]
    liste = []
    for i in range(2, 6):
        data[i] = data[i].strip().split(",")
        del data[i][-1]
        liste.append([state.strip() for state in data[i]])
        

print(bpm)
print(tones)
print(liste)