import matplotlib.pyplot as plt

f = open("log1.txt", "r")
i = 0
line_total = 0
samples = 20
sample = []

for line in f:
    i += 1
    if(i % 20 == 0):
        #plt.scatter(i, float(line_total))
        sample.append(line_total)
        line_total = 0
    else:
        line_total += float(line)/samples

plt.figure(0)
label1 = 'Aceleração   max = ' +  str( int(max(sample))) + " m/s^2"
plt.plot(sample, label = label1)
f.close()
plt.legend()

f = open("log2.txt", "r")
i = 0
line_total = 0
samples = 20
sample = []

for line in f:
    i += 1
    if(i % 20 == 0):
        #plt.scatter(i, float(line_total))
        sample.append(line_total)
        line_total = 0
    else:
        line_total += float(line)/samples

plt.figure(1)
label1 = 'Força   max = ' +  str( int(max(sample))) + " N"
plt.plot(sample, label = label1)
f.close()
plt.legend()

plt.show()