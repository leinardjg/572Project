import sys
from github import Github

token = ''
github = Github(token)

NODESFILENAME = "nodes.csv"
EDGESFILENAME = "edges.csv"

if len(sys.argv) != 2:
    print("Provide one file name containing the nodes table.")

n = 2
m = 3

nodesFile = open(NODESFILENAME, 'r')
edgesFile = open(EDGESFILENAME, 'w+')

users = set()

print("Creating dictionary...", end='')

for line in nodesFile:

    user = [x.strip() for x in line.split(',')][0]
    users.add(user)

nodesFile.close()

print("DONE")

counter = 0

nodesFile = open(NODESFILENAME, 'r')

print("Getting followings...")
print(f"User count: {len(users)}")

for line in nodesFile:
    if counter < n * (len(users) / m):
        counter += 1
        continue
    elif (counter < (n + 1) * len(users) / m):
        user = [x.strip() for x in line.split(',')][0]
        following = github.get_user(user).get_following()

        for f in following:
            if f.login in users:
                edgesFile.write(f"{user}, {f.login}\n")
        
        counter += 1
    else:
        break

nodesFile.close()
edgesFile.close()