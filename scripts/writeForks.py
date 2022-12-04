from datetime import datetime
import time

from dotenv import dotenv_values
from github import Github
from github.GithubException import (RateLimitExceededException,
                                    UnknownObjectException)

CONFIG = dotenv_values(".env")
NODESFILEPATH = "./final/followers_network/nodes_repo_community.csv"
START = 2750
NODESOUTPUTPATH = "./forks_4b.csv"

print(f"Time is {datetime.now()}")
time.sleep(3)

# wait for 1h10m
SECONDSTOWAIT = 4200

github = Github(CONFIG["GH_TOKEN"])

nodesFile = open(NODESFILEPATH, 'r')

users = []

print("Reading seed file...", end='', flush=True)

nodesFile.readline()

for line in nodesFile:
    userInfo = [x.strip() for x in line.split(',')]
    user = userInfo[0]
    userCommunity = int(userInfo[2])
    if (userCommunity > -1):
        users.append(user)
    else:
        print(f"Excluded: {user}")

nodesFile.close()

print("DONE")

# for testing
time.sleep(3)

print("Working...")

counter = START

outputFile = open(NODESOUTPUTPATH, 'w')

while counter < len(users):

    try:

        user = users[counter]
        repos = github.get_user(user).get_repos()
        for repo in repos:
            try:
                if (repo.fork):
                    otherUser = repo.parent.owner.login
                    if otherUser in users:
                        outputFile.write(f"{user}, {otherUser}\n")

            except RateLimitExceededException as rateLimitE:

                print(f"API Limit Reached. Finished line {counter - 1}. Will try again in a bit...")
                time.sleep(SECONDSTOWAIT / 2)
                print(f"Retrying in {SECONDSTOWAIT / 2} seconds...")
                time.sleep(SECONDSTOWAIT / 2)
                print("Working...")
                pass

            except UnknownObjectException as exception404:
                print(f"404 on user {user}")
                pass

            except Exception as e:
                print(f"Exception {type(e)} on user {user}: ")
                print(e)
                pass

    except RateLimitExceededException as rateLimitE:

        print(f"{datetime.now()} API Limit Reached. Finished line {counter - 1}. Will try again in a bit...")
        time.sleep(SECONDSTOWAIT / 2)
        print(f"{datetime.now()} Retrying in {SECONDSTOWAIT / 2} seconds...")
        time.sleep(SECONDSTOWAIT / 2)
        print("Working...")
        pass

    except UnknownObjectException as exception404:
        print(f"404 on user {user}")
        pass

    except Exception as e:
        print(f"Exception {type(e)} on user {user}: ")
        print(e)
        pass
        
    counter += 1

outputFile.close()

print("DONE")