from models import Vote

OPTIONS = ("input","radio","select","slider")

for o in OPTIONS:
    for i in range(1,11):
        print o
        print i
        Vote(number=i,method=o).put()




from google.appengine.api.labs import taskqueue
number = 1
method = "input"
params = {
    "number": number,
    "method": method,
    "cursor": None,
    "refresh": True,
}
taskqueue.add(url="/tasks", params=params)
print method, number