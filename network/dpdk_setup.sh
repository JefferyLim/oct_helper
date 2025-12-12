sudo ovs-vsctl add-br br-dpdk -- set bridge br-dpdk datapath_type=netdev
sudo ovs-vsctl add-port br-dpdk vhost-user-client0 -- set Interface vhost-user-client0 type=dpdkvhostuser
sudo ovs-vsctl add-port br-dpdk vhost-user-client1 -- set Interface vhost-user-client1 type=dpdkvhostuser


sudo ovs-vsctl set Interface vhost-user-client0 mtu_request=9000
sudo ovs-vsctl set Interface vhost-user-client0 mtu_request=9000
sudo ovs-vsctl set Interface br-dpdk mtu_request=9000


# change /etc/libvirt/qemu.confg user/group to root
#

FILE="/etc/libvirt/qemu.conf"

# add user="root" if missing
grep -q '^user="root"' "$FILE" || echo 'user="root"' >> "$FILE"

# add group="root" if missing
grep -q '^group="root"' "$FILE" || echo 'group="root"' >> "$FILE"
