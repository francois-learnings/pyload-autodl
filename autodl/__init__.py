"""Module docstring.
TODO
"""
import sys, getopt, time, os
import autodl.scheduler
import autodl.utils

def usage():
    print """Usage: 

autodl <options>

Options: 
    -c config_file (ie: /etc/autodl/config.json)
    -s user_settings_file (ie: /etc/autodl/user_settings.json)
    -a pyload_server_ip_address (ie: 192.168.0.12) 
    -P pyload_server_port (default: 8000) 
    -u pyload_user 
    -p pyload_user_password 
"""



def parse_options():
    # parse command line options
    DICT_OPTS = {}
    DICT_OPTS["CONFIG_FILE"] = os.getenv('ODL_CONFIG', None)
    DICT_OPTS["USER_SETTINGS_FILE"] = os.getenv('ODL_USER_SETTINGS', None)
    DICT_OPTS["SERVER_IP"] = os.getenv('ODL_SERVER_IP', None)
    DICT_OPTS["SERVER_PORT"] = os.getenv('ODL_SERVER_PORT', None)
    DICT_OPTS["USER"] = os.getenv('ODL_USER', None)
    DICT_OPTS["PASSWORD"] = os.getenv('ODL_PASSWORD', None)

    #print sys.argv
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:s:a:P:u:p:h", ["help", 
            "config-file=", "settings=", "address=", "port=", "user=", 
            "password="])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)

    # process options
    warning_option_msg = ("Warning ! The environment variable \"%s\" is \
                  BUT the value will be overwritten because of the \
                  parameter \"%s\"")        
   
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-c", "--config-file"):
            if DICT_OPTS["CONFIG_FILE"] is not None:
                print (warning_option_msg) % ("$CONFIG_FILE", o)

            CONFIG_FILE=a
            #print CONFIG_FILE
            DICT_OPTS["CONFIG_FILE"]=CONFIG_FILE
        elif o in ("-s", "--settings"):
            if DICT_OPTS["USER_SETTINGS_FILE"] is not None:
                print (warning_option_msg) % ("USER_SETTINGS_FILE", o)
                
            USER_SETTINGS_FILE=a
            #print USER_SETTINGS_FILE
            DICT_OPTS["USER_SETTINGS_FILE"]=USER_SETTINGS_FILE
        elif o in ("-a", "--address"):
            if DICT_OPTS["SERVER_IP"] is not None:
                print (warning_option_msg) % ("SERVER_IP", o)
                
            SERVER_IP=a
            #print SERVER_IP
            DICT_OPTS["SERVER_IP"]=SERVER_IP
        elif o in ("-P", "--port"):
            if DICT_OPTS["SERVER_PORT"] is not None:
                print (warning_option_msg) % ("SERVER_PORT", o)

            SERVER_PORT=a
            #print SERVER_PORT
            DICT_OPTS["SERVER_PORT"]=SERVER_PORT
        elif o in ("-u", "--user"):
            if DICT_OPTS["USER"] is not None:
                print (warning_option_msg) % ("USER", o)
                
            USER=a
            #print USER
            DICT_OPTS["USER"]=USER
        elif o in ("-p", "--password"):
            if DICT_OPTS["PASSWORD"] is not None:
                print (warning_option_msg) % ("PASSWORD", o)
               
            PASSWORD=a
            #print PASSWORD
            DICT_OPTS["PASSWORD"]=PASSWORD
    return DICT_OPTS

def set_defaults(DICT_OPTS):
    """
    set a default value for some optionnal parameter if they're not already set
    """
    for k in DICT_OPTS:
        #print k
        if DICT_OPTS[k] is None:
            #print DICT_OPTS[k]
            if k == "SERVER_PORT":
                DICT_OPTS["SERVER_PORT"] = "8000"
            else:
                #logger.error("No value set for %s") % (k)
                raise ValueError("No value set for %s" % (k))

def main():
    DICT_OPTS = parse_options()
    set_defaults(DICT_OPTS)
    autodl.utils.set_globals(DICT_OPTS)
    #print settings.CONFIG_FILE
    #print DICT_OPTS
    sched = autodl.scheduler.Scheduler(DICT_OPTS)
    sched.run()
    while True:
            time.sleep(1)


if __name__ == "__main__":
    main()
