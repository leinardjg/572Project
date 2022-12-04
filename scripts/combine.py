import sys
import os.path

FILENAME = 'nodes.csv'

if (len(sys.argv) < 2):
    print("Provide file names as arguments.")
    sys.exit()

for arg in sys.argv:
    if (os.path.isfile(arg) == False):
        print(f"File \"{arg}\" does not exist.")
        sys.exit()

users = {}

for arg in sys.argv[1:]:

    print(f"Processing \"{arg}\"...", end='')

    file = open(arg)

    for line in file:

        record = [x.strip() for x in line.split(',')]
        record[1] = int(record[1])
    
        if record[0] in users:
            users[record[0]] += record[1]
        else:
            users[record[0]] = record[1]

    print("DONE")

# write to file

file = open(FILENAME, 'w+')
print(f"Writing users to \"{FILENAME}\"...", end='')

for user in users:
    file.write(f"{user}, {users.get(user)}\n")

print("DONE")
