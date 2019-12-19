import subprocess
import typing
from datetime import datetime

def installFromTxt(path: str, log=True):
    packages = {}
    errorCount = 0
    with open(path, "r") as f:
        for line in f:
            packages[line.strip()] = {
                "Success": False,
                "Proccess": None,
                "Message" : "",
            }

    queue = list(packages.keys())
    for pkgName in queue:
        process = subprocess.Popen(['pip3', 'install', pkgName],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        packages[pkgName]["Process"] = process

    pkgFinishedCount = 0
    while queue:
        pkgName = queue.pop(0)
        process = packages[pkgName]["Process"]
        if process.poll() == None:
            queue.append(pkgName)

        else:
            pkgFinishedCount += 1
            stdout, stderr = process.communicate()
            print(pkgName)
            if stderr:
                errorCount += 1
                packages[pkgName]["Message"] = "    " + str(stderr).replace("\\n", "\n    ")
            else:
                packages[pkgName]["Success"] = True
                packages[pkgName]["Message"] = "    " + str(stdout).replace("\\n", "\n    ")
            print(f"Progress: {pkgFinishedCount} : {len(packages)}")
    
    if errorCount > 0:
        success = {}
        failed = {}
        for pkgName in packages:
            if packages[pkgName]["Success"]:
                success[pkgName] = packages[pkgName]["Message"]
            else:
                failed[pkgName] = packages[pkgName]["Message"]

        
        logFileName = f"Installation log {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt"
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


    else:
        print("Succesfully installed all packages")


if __name__ == "__main__":
    installFromTxt("packages.txt")
