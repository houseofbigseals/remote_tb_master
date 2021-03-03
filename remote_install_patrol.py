import time
import os
import datetime
import paramiko
from scp import SCPClient

def install_to_one_tb(host, username, passwd):

    print("installing soft on robot {}".format(host))

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname=host, username=username, password=passwd,
                     look_for_keys=False, allow_agent=False)

    print("\n wait for cloning patrol pkg \n")

    build_pkg = "sudo ./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release " \
                  "--install-space /opt/ros/melodic --pkg=turtlebro_patrol"

    stdin, stdout, stderr = client.exec_command("cd /home/pi/ros_catkin_ws/src &&"
                                                "git clone https://github.com/voltbro/turtlebro_patrol;"
                                                , timeout=15, get_pty=True)
    print(str(stdout.read() + stderr.read(), 'utf-8'))

    time.sleep(10)


    print(str('try to build patrol pkg and run it\n'))
    stdin, stdout, stderr = client.exec_command("source /opt/ros/melodic/setup.bash;" +
                                                "cd ~/ros_catkin_ws/;" +
                                                ("sudo -S -p '' {0};".format(build_pkg))
                                                , timeout=20, get_pty=True)
    stdin.write('brobro' + "\n")
    stdin.flush()
    time.sleep(10)

    print(str(stdout.read() + stderr.read(), 'utf-8'))
    client.close()

if __name__ == "__main__":
    # host = 'turtlebro12.local'
    username = 'pi'
    passwd = 'brobro'

    # robots = ['192.168.1.61']
    robots = ['192.168.1.137']
    # robots2 = ['192.168.1.65, 192.168.1.93, 192.168.1.77, 192.168.1.135', '192.168.1.124']

    for host in robots:
        install_to_one_tb(host, username, passwd)