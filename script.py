import subprocess
import typing
from datetime import datetime
import os


def printProgressBar(finishedCount: int, total: int):
    columns = int(os.popen("stty size", "r").read().split()[1])

    columns = columns - len("progress ") - len(f" {finishedCount}/{total}") - len("100%")
    percentageDone = finishedCount / total
    bar = "\u2588" * int(columns * percentageDone) + "\u2591" * int(columns * (1 - percentageDone))
    toPrint = "progress " + bar + f"{finishedCount}/{total} " + str(int(percentageDone * 100)) + "%"
    print(toPrint, flush=True, end="")
    return len(toPrint)


def installFromTxt(path: str, log: bool=True):
    packages = {}
    errorCount = 0
    print("Reading packages to install")
    with open(path, "r") as f:
        for line in f:
            packages[line.strip()] = {
                "Success": False,
                "Proccess": None,
                "Message" : "",
            }

    queue = list(packages.keys())
    
    print("Installing: ")
    for pkgName in queue:
        print("\t" + pkgName)

    for pkgName in queue:
        process = subprocess.Popen(['pip3', 'install', pkgName],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        packages[pkgName]["Process"] = process


    
    pkgFinishedCount = 0
    barLength = printProgressBar(pkgFinishedCount, len(packages))

    while queue:
        pkgName = queue.pop(0)
        process = packages[pkgName]["Process"]
        if process.poll() == None:
            queue.append(pkgName)

        else:
            pkgFinishedCount += 1
            stdout, stderr = process.communicate()
            # print(pkgName)
            if stderr:
                errorCount += 1
                packages[pkgName]["Message"] = "    " + stderr.decode().replace("\\n", "\n    ")
            else:
                packages[pkgName]["Success"] = True
                packages[pkgName]["Message"] = "    " + stdout.decode().replace("\\n", "\n    ")
            for i in range(barLength): print("\b", flush=True, end="")
            printProgressBar(pkgFinishedCount, len(packages))
    print()

    if errorCount > 0:
        success = {}
        failed = {}
        for pkgName in packages:
            if packages[pkgName]["Success"]:
                success[pkgName] = packages[pkgName]["Message"]
            else:
                failed[pkgName] = packages[pkgName]["Message"]

        
        logFileName = f"Installation-log-{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt"
        with open(logFileName, "w") as f:
            f.write("Failed installations:\n")
            for pkgName in failed:
                f.write("\nPackage: " + pkgName + "\n")
                f.write(failed[pkgName])
            
            f.write("\nSuccessful installations:\n")
            for pkgName in success:
                f.write("\nPackage: " + pkgName + "\n")
                f.write(success[pkgName])


        print("Successfully installed:")
        for pkgName in success:
            print(f"\t{pkgName}")

        print("Failed to install:")
        for pkgName in failed:
            print(f"\t{pkgName}")

        print("See")
        print(f"\t{logFileName}")
        print("for details")


    else:
        print("Succesfully installed all packages")


if __name__ == "__main__":
    installFromTxt("packages.txt")
