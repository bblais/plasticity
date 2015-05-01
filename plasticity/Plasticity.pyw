#!/usr/bin/env python
import sys
from optparse import OptionParser
import plasticity


parser = OptionParser()
parser.add_option( "--nosplash", 
              action="store_false", dest="splash", default=True,
              help="don't show the splash screen")
parser.add_option( "--server", 
            action="store_true", dest="server", default=False,
            help="Run an xml-rpc server")
(options, args) = parser.parse_args()

if len(args)>=1:
    lfname=args[0]
else:
    lfname=None

if options.server:
    port=4242
    from SimpleXMLRPCServer import SimpleXMLRPCServer
    SimpleXMLRPCServer.allow_reuse_address = 1

    server = SimpleXMLRPCServer(("", port))
    server.register_function(plasticity.run_sim_mod.run_sim_server) 
    
    try:
        print "Serving on port %d..." % port
        server.serve_forever() # Start the server
    finally:
        print "done."
        server.server_close()

else:
    plasticity.run(lfname,None,options.splash)

