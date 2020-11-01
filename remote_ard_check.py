
import time
import os
import datetime
import paramiko
from scp import SCPClient

def ard_test(host, user, passwd):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname=host, username=user, password=passwd,
                   look_for_keys=False, allow_agent=False)


    # 1. load hex files to remote robot

    # SCPCLient takes a paramiko transport as an argument
    scp = SCPClient(client.get_transport())

    output_name1 =  'hex1.ino.mega.hex'
    output_name2 = 'hex2.ino.mega.hex'

    scp.put('./bin/amg88xx_main.ino.mega.hex', output_name1)
    scp.put('./bin/Blink.ino.mega.hex', output_name2)
    # scp.get('test2.txt')

    scp.close()

    # Uploading the 'test' directory with its content in the
    # '/home/user/dump' remote directory
    # scp.put('test', recursive=True, remote_path='/home/user/dump')

    # 2. use avrdude to write hex1 to arduino
    # avrdude -v -v -p atmega2560 -c wiring -P
    # /dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0
    # -b 115200 -D -U flash:w:sketch_mar24a.ino.mega.hex:i

    avrdude_cmd_1 = "avrdude -v -v -p atmega2560 -c wiring -P " + \
    "/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0" + \
    " -b 115200 -D -U flash:w:{}:i".format(output_name1)

    avrdude_cmd_2 = "avrdude -v -v -p atmega2560 -c wiring -P " + \
    "/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0" + \
    " -b 115200 -D -U flash:w:{}:i".format(output_name2)

    topic_name = "/amg88xx_pixels"

    print(avrdude_cmd_1)

    stdin, stdout, stderr = client.exec_command("source /opt/ros/melodic/setup.bash;"
                                                    "ls | grep hex;"
                                                    "rostopic list;"
                                                    "sudo -S -p '' {0}".format(avrdude_cmd_1)
                                                    , timeout=20, get_pty=True)
    stdin.write('brobro' + "\n")
    stdin.flush()

    print(str(stdout.read() + stderr.read(), 'utf-8'))



    # 3. check rostopic list and check that topics work

    for i in range(0, 10):
        time.sleep(1)
        print("waiting for ros to find arduino node ...")

    stdin, stdout, stderr = client.exec_command("source /opt/ros/melodic/setup.bash;"
                                                "rostopic list;"
                                                "rostopic pub --once /alarm_led std_msgs/Bool 'data: true'; "
                                                "rostopic echo -n 1 {}".format(topic_name)
                                                ,timeout=8, get_pty=True)

    print(str(stdout.read() + stderr.read(), 'utf-8'))

    input("\n Check if red lamp on, and press Enter to continue...")

    print("check done, start cleaning")

    # 4. use avrdude to write blink to arduino

    stdin, stdout, stderr = client.exec_command("source /opt/ros/melodic/setup.bash;"
                                                "rostopic pub --once /alarm_led std_msgs/Bool 'data: false'; "
                                                "ls | grep hex;"
                                                "rostopic list;"
                                                "sudo -S -p '' {0};"
                                                "rosnode kill /arduino_serial_node".format(avrdude_cmd_2)
                                                , timeout=20, get_pty=True)
    stdin.write('brobro' + "\n")
    stdin.flush()

    print(str(stdout.read() + stderr.read(), 'utf-8'))

    # 5. check rostopic list again

    for i in range(0, 10):
        time.sleep(1)
        print("waiting for ros to find that there are no more any arduino node ...")

    stdin, stdout, stderr = client.exec_command("source /opt/ros/melodic/setup.bash;"
                                                "rostopic list"
                                                ,timeout=5, get_pty=True)

    print(str(stdout.read() + stderr.read(), 'utf-8'))

    # 6. rm hex files from robot

    stdin, stdout, stderr = client.exec_command("rm {0}; rm {1};"
                                                "ls | grep hex;".format(
                                                output_name1, output_name2)
                                                ,timeout=5, get_pty=True)

    print(str(stdout.read() + stderr.read(), 'utf-8'))





if __name__ == "__main__":
    # host = 'turtlebro12.local'
    username = 'pi'
    passwd = 'brobro'

    robots = ['10.8.0.6']

    for host in robots:
        ard_test(host, username, passwd)