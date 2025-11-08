echo 2048 | sudo tee /proc/sys/vm/nr_hugepagesi

sudo mkdir -p /mnt/huge
sudo mount -t hugetlbfs nodev /mnt/huge

sudo ovs-vsctl add-port br-dpdk vhost-user-client0 -- set Interface vhoset-user-client0 type=dpdkvhostuser

# change /etc/libvirt/qemu.confg user/group to root
#

