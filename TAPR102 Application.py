import subprocess

# Define the commands for each program
command1 = ["python", "SQL_Write.py"]
# command2 = ["python", "GUI_8.py"]

process1 = subprocess.Popen(command1)

#process1 = subprocess.Popen(["pythonw", "SQL_Write.py"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

process2 = subprocess.Popen(["pythonw", "GUI_10.py"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

process1.wait()

if process2.terminate():
    process1.terminate()

    process2.wait()

print("Both programs have finished.")


