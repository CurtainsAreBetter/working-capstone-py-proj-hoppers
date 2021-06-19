"""
You ever try the build a tall spaghetti tower challenge?
Well if you have, you were probably pragmatic about it.
But you'll find, that gradeschoolers will usually do better than
your average high-school student or most anyone past that age.
That's because instead of taking time to plan ahead they just work around
the problems they create for themselves.
Which works... because it's a spaghetti tower.
This is my spaghetti tower.
"""


import json, pwn

def makeDictFromFile(filenam):
    thefile = open(filenam)
    tfr = thefile.readline()
    d = {}
    while tfr:
        tfr = tfr.strip("\n")
        tfr = tfr.split(" ")
        d[tfr[0]] = tfr[1]
        tfr = thefile.readline()
    thefile.close()
    return d


for i in range(6):
    cfgname = "bandit"+str(i)+".cfg"
    with open(cfgname) as f:
        jd = json.load(f)
        if jd["password"] is None:
            passw = makeDictFromFile("passwords.txt")[str(i)]
        else:
            passw = jd["password"]
        shell = pwn.ssh(user=jd["username"], host=jd["address"], port=jd["port"],
                        password=passw)
        for cmd in jd["commands"]:
            newpass = shell[cmd]
        newpass = str(newpass)
        newpass = newpass.strip(" ")
        pf = open("passwords.txt", "a")
        pf.write(str(int(jd["username"][-1:]) + 1) + " " + newpass[2:len(str(newpass))-1] + "\n")
        pf.close()
        shell['exit']
