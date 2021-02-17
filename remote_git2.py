
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

    stdin, stdout, stderr = client.exec_command("sudo -S -p '' apt-get install python-pip -y", timeout=15)
    stdin.write('brobro' + "\n")
    stdin.flush()
    time.sleep(15)
    print(str(stdout.read() + stderr.read(), 'utf-8'))

    stdin, stdout, stderr = client.exec_command("sudo -S -p '' apt-get install python-tqdm -y", timeout=15)
    stdin.write('brobro' + "\n")
    stdin.flush()
    time.sleep(15)

    # --force - yes
    print(str(stdout.read() + stderr.read(), 'utf-8'))

    print("\n wait for ws_service_pkg_1 \n")

    build_pkg = "sudo ./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release " \
                  "--install-space /opt/ros/melodic --pkg=ws_service_pkg_"
    build_pkg_1 = build_pkg + "1"
    build_pkg_2 = build_pkg + "2"
    build_pkg_3 = build_pkg + "3"


    stdin, stdout, stderr = client.exec_command("cd /home/pi/ros_catkin_ws/src && echo 'in src';"
                                                "rm -rf ~/ros_catkin_ws/src/ws_service_pkg_1 &&"
                                                "git clone https://github.com/voltbro/ws_service_pkg_1.git;"
                                                "cd ~/ros_catkin_ws/src/ws_service_pkg_1 && echo 'in ws_service_pkg_1';"
                                                " ls ;"
                                                "git reset --hard 527ff5b4e2520c26a095a359055a514ec5d5ca16 &&"
                                                " echo 'hm:'"
                                                , timeout=15, get_pty=True)
    print(str(stdout.read() + stderr.read(), 'utf-8'))
    # build pkg and test it
    print(str('try to build pkg1 and run it\n'))
    stdin, stdout, stderr = client.exec_command("source /opt/ros/melodic/setup.bash;" +
                                                "cd ~/ros_catkin_ws/;" +
                                                ("sudo -S -p '' {0};".format(build_pkg_1)) +
                                                "roslaunch ws_service_pkg_1 configure.launch"
                                                , timeout=20, get_pty=True)
    stdin.write('brobro' + "\n")
    stdin.flush()
    time.sleep(10)

    print(str(stdout.read() + stderr.read(), 'utf-8'))

    print("\n wait for ws_service_pkg_2! \n")

    stdin, stdout, stderr = client.exec_command("cd /home/pi/ros_catkin_ws/src && echo 'in src';"
                                                "rm -rf ~/ros_catkin_ws/src/ws_service_pkg_2 &&"
                                                "git clone https://github.com/voltbro/ws_service_pkg_2.git;"
                                                "cd ~/ros_catkin_ws/src/ws_service_pkg_2 && echo 'in ws_service_pkg_2';"
                                                " ls ;"
                                                "git reset --hard 6df7f52628348cce744b83fd8558eac3a87278b3 &&"
                                                "echo 'wait, try user script:'"
                                                , timeout=25, get_pty=True)
    print(str(stdout.read() + stderr.read(), 'utf-8'))

    # build pkg and test it
    print(str('try to build pkg2 and run it\n'))
    stdin, stdout, stderr = client.exec_command("source /opt/ros/melodic/setup.bash;" +
                                                "cd ~/ros_catkin_ws/;" +
                                                ("sudo -S -p '' {0};".format(build_pkg_2)) +
                                                "roslaunch ws_service_pkg_2 configure.launch"
                                                , timeout=20, get_pty=True)
    stdin.write('brobro' + "\n")
    stdin.flush()
    time.sleep(10)
    print(str(stdout.read() + stderr.read(), 'utf-8'))

    print("\n wait more, ws_service_pkg_3! \n")

    stdin, stdout, stderr = client.exec_command("cd /home/pi/ros_catkin_ws/src && echo 'in src';"
                                                "rm -rf ~/ros_catkin_ws/src/ws_service_pkg_3 &&"
                                                "git clone https://github.com/voltbro/ws_service_pkg_3.git;"
                                                "cd ~/ros_catkin_ws/src/ws_service_pkg_3 && echo 'in ws_service_pkg_3';"
                                                " ls ;"
                                                "echo 'wait, try user script:' "
                                                , timeout=25, get_pty=True)
    print(str(stdout.read() + stderr.read(), 'utf-8'))

    # build pkg and test it
    print(str('try to build pkg3 and run it\n'))
    stdin, stdout, stderr = client.exec_command("source /opt/ros/melodic/setup.bash;" +
                                                "cd ~/ros_catkin_ws/;" +
                                                ("sudo -S -p '' {0};".format(build_pkg_3)) +
                                                "roslaunch ws_service_pkg_3 configure.launch"
                                                , timeout=40, get_pty=True)
    stdin.write('brobro' + "\n")
    stdin.flush()
    time.sleep(10)
    print(str(stdout.read() + stderr.read(), 'utf-8'))

    client.close()
    # rc_comm = "source /opt/ros/melodic/setup.bash; nohup roslaunch ros_pkg test.launch &"


if __name__ == "__main__":
    # host = 'turtlebro12.local'
    username = 'pi'
    passwd = 'brobro'

    # robots = ['192.168.1.61']
    robots = ['192.168.1.93']
    robots2 = ['192.168.1.65, 192.168.1.93, 192.168.1.77, 192.168.1.135', '192.168.1.124']

    for host in robots:
        install_to_one_tb(host, username, passwd)

    # cd ~/ros_catkin_ws/
    # sudo ./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release --install-space /opt/ros/melodic --pkg=ws_service_pkg_1
    #