from random import randint

counts = [0 for n in range(10)]

def go():
    choice = randint(1,10)
    print choice
    counts[choice-1] += 1

[go() for n in xrange(10000)]

print counts

max = max(counts)
print max

i = 1
for c in counts:
    #(10/int((float(c)/float(max))))
    p = int((float(c)/max) * 100)
    graph = "".join(["*" for x in range(0,p)])
    print '%s\t: %s\t%s' % (i, c, graph)
    i += 1
