import controller
import socket
import sys
from termcolor import colored
import _thread


class SocketHandler():
    def __init__(self, logger):
        try:
            self.logger = logger

            self.port = 1512
            self.packet_size = 2048

            self.sock = socket.socket()
            print(f'connecting to socket server ... ', end='')
            self.sock.connect(('localhost', self.port))
            print(colored('OK!', 'green'))
            _thread.start_new_thread(self.check_incoming_commands, ())

        except KeyboardInterrupt:
            self.sock.close()
            exit(0)
        except ConnectionRefusedError:
            print(colored('FAILED: connection refused', 'red'))

    def check_incoming_commands(self):
        """
        Checks for incoming commands from socket server
        :return: None
        """
        try:
            while True:
                data = self.sock.recv(self.packet_size)
                if data.decode() == '':
                    self.sock.close()
                    print('socket closed')
                    break
                else:
                    self.classify_command(data.decode().replace('\n', ''))
        except Exception as err:
            method_name = sys._getframe().f_code.co_name
            self.logger.write_to_log('exception', 'controller')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'socket handler')

    def classify_command(self, msg):
        """
        Classifies command got from socket
        :param msg: data received from socket
        :return: None
        """
        try:
            msg = msg.split('-')

            if msg[0] == 'event_registered':
                _thread.start_new_thread(controller.notify_about_event_request, ())   # !!ATTENTION!! if one event request is currently processing, it won't work
            elif msg[0] == 'feedback_updated': # -event_id
                _thread.start_new_thread(controller.notify_about_feedback_update, (msg[1],))
            # TODO: add some cross-bot interacting commands
        except Exception as err:
            method_name = sys._getframe().f_code.co_name
            self.logger.write_to_log('exception', 'controller')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'socket handler')

    def send_socket_command(self, msg):
        """
        Sends command to another bot via socket server
        :param msg:command to pass
        :return: None
        """
        try:
            self.sock.send(msg.encode())
            self.logger.write_to_log('socket message sent', 'socket handler')
        except Exception as err:
            method_name = sys._getframe().f_code.co_name
            self.logger.write_to_log('exception', 'controller')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'socket handler')



