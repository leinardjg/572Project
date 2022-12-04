from github import Github
import sys

# names
NODESFILENAME = "nodes.csv"

# your token here
token = ''
github = Github(token)

# define your repos here
myRepos = []

reposDictionary = {
   'laravel/laravel' : 1,
   'django/django' : 2,
   'pallets/flask' : 4,
   'expressjs/express' : 8,
   'rails/rails' : 16,
   'spring-projects/spring-framework' : 32,
   'nestjs/nest' : 64,
   'meteor/meteor' : 128,
   'strapi/strapi' : 256,
   'koajs/koa' : 512,
   'beego/beego' : 1024,
   'symfony/symfony' : 2048,
   'kataras/iris' : 4096,
   'bcit-ci/CodeIgniter' : 8192,
   'dotnet/core' : 16384
}

# check repos
for repo in myRepos:
    if repo not in reposDictionary:
        print(f"Repository {repo} not in dictionary.")
        sys.exit()

# dictionary of all users
allUsers = {}

# get all users and add them to a set
for repo in myRepos:

    print(f"Obtaining \"{repo}\" contributors...")

    contributors = github.get_repo(repo).get_contributors()
    currentMask = reposDictionary.get(repo)

    for user in contributors:
        if user.login in allUsers:
            allUsers[user.login] += currentMask
        else:
            allUsers[user.login] = currentMask

print("Writing to file...")

# write the set into a file
nodesFile = open(NODESFILENAME, 'w+')

for user in allUsers:
    nodesFile.write(f"{user}, {allUsers.get(user)}\n")

nodesFile.close()
print("DONE")