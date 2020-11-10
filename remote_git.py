
import re
import time
import os
import datetime
import paramiko
import os

def remote_command(command, host, username, passwd):
    """
    execute remote command
    :param command:
    :param host:
    :param username:
    :param passwd:
    :return:
    """

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname=host, username=username, password=passwd,
                   look_for_keys=False, allow_agent=False)

    # ssh = client.invoke_shell()
    # stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    try:
        stdin, stdout, stderr = client.exec_command(command, timeout=5)
        data = stdout.read() + stderr.read()
    except Exception as e:
        print("remote_command: we got err: {}".format(e))
        data = "we got no data"
    time.sleep(1)
    client.close()
    return data


def install_to_one_tb(host, username, passwd):

    print("installing soft on robot {}".format(host))
    # so much  monkey code

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname=host, username=username, password=passwd,
                     look_for_keys=False, allow_agent=False)

    git_addr_1 = 'ws_service_pkg_1'
    git_addr_2 = 'ws_service_pkg_2'
    git_addr_3 = 'ws_service_pkg_3'

    stdin, stdout, stderr = client.exec_command("sudo -S -p '' apt-get install python-pip -y", timeout=5)
    stdin.write('brobro' + "\n")
    stdin.flush()
    # --force - yes
    print(str(stdout.read() + stderr.read(), 'utf-8'))

    print("\n wait for ws_service_pkg_1 \n")

    stdin, stdout, stderr = client.exec_command("cd /home/pi/ros_catkin_ws/src && echo 'in src';"
                                                "rm -rf ~/ros_catkin_ws/src/ws_service_pkg_1 &&"
                                                "git clone https://github.com/voltbro/ws_service_pkg_1.git;"
                                                "cd ~/ros_catkin_ws/src/ws_service_pkg_1 && echo 'in ws_service_pkg_1';"
                                                " ls ;"
                                                "git reset --hard bd985b9be0241962b94295d63a51970925d7a456 &&"
                                                " echo 'wait, try user script:' && ./run/configure.sh"
                                                , timeout=5, get_pty=True)
    print(str(stdout.read() + stderr.read(), 'utf-8'))

    print("\n wait for ws_service_pkg_2! \n")

    stdin, stdout, stderr = client.exec_command("cd /home/pi/ros_catkin_ws/src && echo 'in src';"
                                                "rm -rf ~/ros_catkin_ws/src/ws_service_pkg_2 &&"
                                                "git clone https://github.com/voltbro/ws_service_pkg_2.git;"
                                                "cd ~/ros_catkin_ws/src/ws_service_pkg_2 && echo 'in ws_service_pkg_2';"
                                                " ls ;"
                                                "git reset --hard 7aa3cbe26ba58b4cd7e16a73f7289802eb11af43 &&"
                                                "echo 'wait, try user script:' && ./run/configure.sh"
                                                , timeout=5, get_pty=True)
    print(str(stdout.read() + stderr.read(), 'utf-8'))

    print("\n wait more, ws_service_pkg_3! \n")

    stdin, stdout, stderr = client.exec_command("cd /home/pi/ros_catkin_ws/src && echo 'in src';"
                                                "rm -rf ~/ros_catkin_ws/src/ws_service_pkg_3 &&"
                                                "git clone https://github.com/voltbro/ws_service_pkg_3.git;"
                                                "cd ~/ros_catkin_ws/src/ws_service_pkg_3 && echo 'in ws_service_pkg_3';"
                                                " ls ;"
                                                "echo 'wait, try user script:' && ./run/configure.sh"
                                                , timeout=5, get_pty=True)
    print(str(stdout.read() + stderr.read(), 'utf-8'))

    client.close()
    # rc_comm = "source /opt/ros/melodic/setup.bash; nohup roslaunch ros_pkg test.launch &"


if __name__ == "__main__":
    # host = 'turtlebro12.local'
    username = 'pi'
    passwd = 'brobro'

    robots = ['turtlebro11.local', 'turtlebro12.local',
              'turtlebro13.local', 'turtlebro14.local', 'turtlebro15.local', 'turtlebro16.local']

    for host in robots:
        install_to_one_tb(host, username, passwd)