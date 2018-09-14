#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import argparse
import os
import sys
import signal
import subprocess
import traceback
import time
import datetime

service = None


def assert_exit(condition, message, code):
    if condition:
        print(message)
        sys.exit(code)


def signal_handler(signal, frame):
    global service
    print("")
    print("You pressed Ctrl + C, force all running threads to exit")
    if service is not None:
        service.stop()
    print("All threads are shutdown gracefully...")


def parse_int(x):
    try:
        return int(x)
    except Exception as e:
        return None


def find_index(parent_dir):
    xs = [ x for x in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, x)) ]
    xs = [ parse_int(x) for x in xs ]
    xs = [ x for x in xs if x is not None ]
    xs.sort()
    return None if len(xs) == 0 else xs[-1]


def get_timestamp_dir(directory):
    directory = '/tmp/timestamp' if directory is None else directory
    # directory = os.path.join(os.environ['YS_DIR'], 'share', 'timestamp') if 'YS_DIR' in os.environ else '/tmp/timestamp'
    try:
        os.makedirs(directory, exist_ok=True)
        return directory
    except OSError as e:
        print(traceback.format_exc())
        return None


def get_system_uptime():
    uptime_seconds = 0
    if sys.platform == 'darwin':
        uptime_seconds = 0
    else:
        with open('/proc/uptime') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_seconds = int(uptime_seconds)
    return uptime_seconds


def listdir_with_fullpath(directory, is_dir=True):
    func = os.path.isdir if is_dir else os.path.isfile
    xs = [ os.path.join(directory, x) for x in os.listdir(directory) ]
    xs = [ x for x in xs if func(x) ]
    return xs


class Service:
    def __init__(self, directory, verbose, interval, record):
        self.directory = directory
        self.verbose = verbose
        self.interval = interval
        self.counter = 0
        self.running = False
        self.index = find_index(directory)
        self.record = record
        self.max_files = 60


    def debug(self, message):
        if self.verbose:
            print(message, flush=True)


    def stop(self):
        self.running = False


    def dump_time(self, directory):
        try:
            uptime = get_system_uptime()
            utc = time.time()
            utc_seconds = int(utc)
            now = datetime.datetime.fromtimestamp(utc)
            day = now.strftime('%Y%m%d')
            sec = now.strftime('%H%M%S')
            tz = time.localtime().tm_zone
            tokens = ["%012d" % (uptime), "%d" % (utc_seconds), day, sec, tz]
            name = "%s.txt" % ("_".join(tokens))
            filepath = os.path.join(directory, name)
            with open(filepath, "w") as f:
                f.write("\t".join(tokens))
            self.debug("create %s" % (filepath))
            subprocess.check_output("sync")
        except Exception as e:
            print(traceback.format_exc())


    def delete_old_files(self, directory):
        xs = [ x for x in os.listdir(directory) ]
        xs = [ x for x in xs if x[-4:] == ".txt" ]
        xs.sort()
        if len(xs) > self.max_files:
            filepath = os.path.join(directory, xs[0])
            try:
                self.debug("delete %s" % (filepath))
                os.remove(filepath)
            except Exception as e:
                print(traceback.format_exc())



    def create_directory(self, directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            print(traceback.format_exc())
            assert_exit(True, "unexpected error to create %s directory, err: %s" % (directory, e), 11)


    def restore_system_time(self):
        index = self.index
        if index is None:
            sys.exit(3)
        else:
            try:
                directory = self.directory
                xs = listdir_with_fullpath(directory)
                xs = [ listdir_with_fullpath(x, False) for x in xs ]
                xs = [ y for x in xs for y in x ]
                xs = [ x for x in xs if x[-4:] == ".txt" ]
                xs.sort()
                # self.debug("found these files ...")
                # [ self.debug("\t%s" % (x)) for x in xs ]
                if len(xs) == 0:
                    self.debug("missing txt files in %s" % (directory))
                    return
                else:
                    xs.sort()
                    zz = xs[-1]
                    nn = os.path.basename(os.path.dirname(zz))
                    zz = os.path.basename(zz)
                    xs = zz.split(".")[0].split("_")
                    if len(xs) < 5:
                        self.debug("insufficient token in filename: %s" % (zz))
                        return
                    else:
                        uptime = int(xs[0])
                        utc = int(xs[1])
                        day = int(xs[2])
                        seconds = int(xs[3])
                        zone = xs[4]
                        self.debug("restore: index = %s" % (nn))
                        self.debug("restore: uptime = %d" % (uptime))
                        self.debug("restore: utc = %d" % (utc))
                        self.debug("restore: day = %d" % (day))
                        self.debug("restore: seconds = %d" % (seconds))
                        self.debug("restore: zone = %s" % (zone))
                        try:
                            command = "date +%%s -s @%d" % utc
                            self.debug("running `%s`" % (command))
                            output = subprocess.check_output(command, shell=True)
                            self.debug("output: %s" % (output))
                            sys.exit(0)
                        except subprocess.CalledProcessError as cpe:
                            print("returncode: %d" % (cpe.returncode))
                            print(traceback.format_exc())
                            sys.exit(5)
            except Exception as e:
                print(traceback.format_exc())
                sys.exit(4)


    def run_daemon(self):
        index = self.index
        index = 0 if index is None else index + 1
        name = "%06d" % index
        directory = os.path.join(self.directory, name)
        with open(self.record, "w") as record_file:
            record_file.write("%d\t%s\n" % (index, name))
        self.debug("directory => %s" % (directory))
        self.debug("index => %s" % (name))
        self.create_directory(directory)
        self.running = True
        while self.running:
            time.sleep(1)
            self.counter = self.counter + 1
            self.counter = 0 if self.counter >= self.interval else self.counter
            if self.counter == 0:
                self.dump_time(directory)
                self.delete_old_files(directory)




def main():
    # Register SIG-INT and C-c events
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="perform the subcommand", type=str)
    parser.add_argument("-d", "--directory", help="the root directory for timestamp logging", type=str, default=None)
    parser.add_argument("-r", "--record", help="the path to the file for writing the number of booting", type=str, default="/tmp/timestamp_logging.idx")
    parser.add_argument("-v", "--verbose", help="verbose messages", default=False, action="store_true")
    parser.add_argument("-i", "--interval", help="time interval for daemon execution", default=300, type=int)
    args = parser.parse_args()

    directory = get_timestamp_dir(args.directory)
    assert_exit(directory is None, "failed to find get_timestamp_dir()", 1)

    global service
    service = Service(directory, args.verbose, args.interval, args.record)
    command = args.command
    if command == "daemon":
        service.run_daemon()
    elif command == "restore":
        service.restore_system_time()
    else:
        assert_exit(True, "unknown command: %s" % (command), 2)



# Entry point
#
if __name__ == '__main__':
    main()
