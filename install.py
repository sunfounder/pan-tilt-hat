import os, sys

def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    print(result)
    # print(status)
    return status, result

# install Tensorflow
    # vilib include Tensorflow
# install vilib
print("install vilib ...")
os.chdir('/home/pi')
if os.path.exists('/home/pi/vilib'):
    # run_command('sudo rm -r vilib/')
    os.chdir('/home/pi/vilib')
    run_command('git pull')
else:
    run_command('git clone https://github.com/sunfounder/vilib.git')
os.chdir('/home/pi/vilib')
run_command('sudo python3 setup.py install')
 

# # install mediapipe-rpi3
# print("install mediapipe-rpi3 ...")
# run_command('sudo pip3 install mediapipe-rpi3')


#install sunfounder_io
print("install sunfounder_io")
os.chdir('/home/pi')
if os.path.exists('/home/pi/sunfounder_io'):
    run_command('sudo rm -r sunfounder_io/')

run_command('git clone https://github.com/sunfounder/sunfounder-io.git')
os.chdir('/home/pi/sunfounder_io')
run_command('sudo python3 setup.py install')

