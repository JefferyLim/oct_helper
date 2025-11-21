echo 2048 | sudo tee /proc/sys/vm/nr_hugepages

sudo mkdir -p /mnt/huge
sudo mount -t hugetlbfs nodev /mnt/huge

sudo ovs-vsctl add-br br-dpdk -- set bridge br-dpdk datapath_type=netdev
sudo ovs-vsctl add-port br-dpdk vhost-user-client0 -- set Interface vhost-user-client0 type=dpdkvhostuser
sudo ovs-vsctl add-port br-dpdk vhost-user-client1 -- set Interface vhost-user-client1 type=dpdkvhostuser


sudo ovs-vsctl set Interface vhost-user-client0 mtu_request=9000
sudo ovs-vsctl set Interface vhost-user-client0 mtu_request=9000
sudo ovs-vsctl set Interface br-dpdk mtu_request=9000

sudo ovs-vsctl add-port br-dpdk host0 -- set Interface host0 type=internal

# change /etc/libvirt/qemu.confg user/group to root
#

