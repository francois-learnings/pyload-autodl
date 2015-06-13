"""Module docstring.
TODO
"""
import sys, getopt, time, os
import autodl.scheduler
import settings

def usage():
    print """Usage: 

autodl <options>

Options: 
    -c config_file (ie: /etc/autodl/autodl_config.json)
    -s pyload_server_ip_address (ie: 192.168.0.12) 
    -P pyload_server_port (default: 8000) 
    -u pyload_user 
    -p pyload_user_password 
"""
def parse_options():
    # parse command line options
    DICT_OPTS = {}
    DICT_OPTS["CONFIG_FILE"] = os.getenv('CONFIG_FILE', None)
    DICT_OPTS["SERVER_IP"] = os.getenv('SERVER_IP', None)
    DICT_OPTS["SERVER_PORT"] = os.getenv('SERVER_PORT', None)
    DICT_OPTS["USER"] = os.getenv('USER', None)
    DICT_OPTS["PASSWORD"] = os.getenv('PASSWORD', None)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:s:P:u:p:h", ["help", "config-file=", "server-ip=", "port=", "user=", "password="])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-c", "--config-file"):
            if DICT_OPTS["CONFIG_FILE"] is not None:
                print "Warning ! The environment variable $CONFIG_FILE is set BUT the value will be overwritten because of the parameter \"-c\""
            CONFIG_FILE=a
            #print CONFIG_FILE
            DICT_OPTS["CONFIG_FILE"]=CONFIG_FILE
        elif o in ("-s", "--server-ip"):
            if DICT_OPTS["SERVER_IP"] is not None:
                print "Warning ! The environment variable $SERVER_IP is set BUT the value will be overwritten because of the parameter \"-s\""
            SERVER_IP=a
            #print SERVER_IP
            DICT_OPTS["SERVER_IP"]=SERVER_IP
        elif o in ("-P", "--port"):
            if DICT_OPTS["SERVER_PORT"] is not None:
                print "Warning ! The environment variable $SERVER_PORT is set BUT the value will be overwritten because of the parameter \"-P\""
            SERVER_PORT=a
            #print SERVER_PORT
            DICT_OPTS["SERVER_PORT"]=SERVER_PORT
        elif o in ("-u", "--user"):
            if DICT_OPTS["USER"] is not None:
                print "Warning ! The environment variable $USER is set BUT the value will be overwritten because of the parameter \"-u\""
            USER=a
            #print USER
            DICT_OPTS["USER"]=USER
        elif o in ("-p", "--password"):
            if DICT_OPTS["PASSWORD"] is not None:
                print "Warning ! The environment variable $PASSWORD is set BUT the value will be overwritten because of the parameter \"-p\""
            PASSWORD=a
            #print PASSWORD
            DICT_OPTS["PASSWORD"]=PASSWORD
    return DICT_OPTS            

def check_opts(DICT_OPTS):
    for k in DICT_OPTS:
        #print k
        if DICT_OPTS[k] is None:
            #print DICT_OPTS[k]
            if k == "SERVER_PORT":
                DICT_OPTS["SERVER_PORT"] = "8000"
            else:
                #logger.error("No value set for %s") % (k)
                raise ValueError("No value set for %s" % (k))

#def set_globals(DICT_OPTS):
#    global CONFIG_FILE
#    CONFIG_FILE = DICT_OPTS["CONFIG_FILE"]

def main():
    DICT_OPTS = parse_options()
    check_opts(DICT_OPTS)
    settings.set_globals(DICT_OPTS)
    #print settings.CONFIG_FILE
    #print DICT_OPTS
    sched = autodl.scheduler.Scheduler(DICT_OPTS)
    while True:
            time.sleep(1)


if __name__ == "__main__":
    main()
