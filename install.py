#!/usr/bin/env python3
import os, sys
import time
import threading

username = os.getlogin()
user_home = os.popen('getent passwd %s | cut -d: -f 6'%username).readline().strip()

errors = []

def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
        # print(status)
    return status, result

at_work_tip_sw = False
def working_tip():
    char = ['/', '-', '\\', '|']
    i = 0
    global at_work_tip_sw
    while at_work_tip_sw:  
            i = (i+1)%4 
            sys.stdout.write('\033[?25l') # cursor invisible
            sys.stdout.write('%s\033[1D'%char[i])
            sys.stdout.flush()
            time.sleep(0.5)

    sys.stdout.write(' \033[1D')
    sys.stdout.write('\033[?25h') # cursor visible 
    sys.stdout.flush()    
        

def do(msg="", cmd=""):
    print(" - %s... " % (msg), end='', flush=True)
    # at_work_tip start 
    global at_work_tip_sw
    at_work_tip_sw = True
    _thread = threading.Thread(target=working_tip)
    _thread.daemon = True
    _thread.start()
    # process run
    status, result = run_command(cmd)
    # print(status, result)
    # at_work_tip stop
    at_work_tip_sw = False
    _thread.join()
    # status
    if status == 0 or status == None or result == "":
        print('Done')
    else:
        print('Error')
        errors.append("%s error:\n  Status:%s\n  Error:%s" %
                      (msg, status, result))

def install():
    # 
    print('Start installing dependencies for Pan-Tilt-HAT:')
    # -------- install vilib --------
    print('- install vilib for \"%s\" ...'%username)
    os.chdir(user_home)
    vilib_flag = False
    if os.path.exists('%s/vilib'%user_home):
        # os.system('sudo rm -r vilib/')
        print('git vilib exists, Whether to delete and re-pull? (y/n)')
        key = input().lower()
        if key == 'y':  # delete and re-pull
            os.system('sudo rm -r vilib/')
            vilib_flag = True
        else:
            print('vilib exists, skip')
            vilib_flag = False
    else:
        vilib_flag = True

    if vilib_flag:
        os.chdir(user_home)
        os.system('git clone -b picamera2 https://github.com/sunfounder/vilib.git')
        os.system('sudo chown -R %s:%s vilib'%(username, username))
        os.chdir(f"{user_home}/vilib")
        os.system('sudo python3 install.py')
    else:
        try:
            import vilib
            print("vilib library import testing ... success")
        except Exception as e:
            print("vilib library import testing ... failure")
            errors.append(f"vilib library import testing error:\n  Error:{e}")

    # -------- install pigpio --------
    do(msg="install pigpio",
        cmd='sudo apt-get update'
        + ' && sudo apt-get install -y python3-pigpio')

    # -------- install gpiozero --------
    # do(msg="install gpiozero",
    #     cmd='sudo apt-get update'
    #     + ' && sudo apt-get install -y python3-gpiozero')

    # check errors
    if len(errors) == 0:
        print("\nFinished")
    else:
        print("\n\nError happened in install process:")
        for error in errors:
            print(error)
        print("Try to fix it yourself, or contact service@sunfounder.com with this message")
        sys.exit(1)


if __name__ == "__main__":
    try:
        install()
    except KeyboardInterrupt:
        print("\nCanceled.")
        sys.stdout.write(' \033[1D')
        sys.stdout.write('\033[?25h') # cursor visible 
        sys.stdout.flush()


