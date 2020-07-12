import os

os.system('ovs-vsctl -- --id=@m create mirror name=mirror1 -- add bridge s1 mirrors @m')

os.system('ovs-vsctl -- --id=@"s1-eth3" get port "s1-eth3" -- set mirror mirror1 select_all=true output-port=@"s1-eth3"')

#os.system('ovs-vsctl clear bridge br0 mirrors')