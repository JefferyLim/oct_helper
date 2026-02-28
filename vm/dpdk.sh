# Install OVS with DPDK
sudo apt install openvswitch-switch-dpdk

# Allocate hugepages
sudo bash -c 'echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages'
sudo mkdir -p /dev/hugepages
sudo mount -t hugetlbfs nodev /dev/hugepages

# Enable DPDK in OVS
sudo ovs-vsctl set Open_vSwitch . other_config:dpdk-init=true
sudo systemctl restart openvswitch-switch

# Create bridge with DPDK datapath
sudo ovs-vsctl add-br dpdkbr0 -- set bridge dpdkbr0 datapath_type=netdev

# Add vhost-user ports
sudo ovs-vsctl add-port dpdkbr0 vhost-server0 \
        -- set Interface vhost-server0 type=dpdkvhostuserclient \
            options:vhost-server-path=/tmp/vhost-server0

sudo ovs-vsctl add-port dpdkbr0 vhost-server1 \
        -- set Interface vhost-server1 type=dpdkvhostuserclient \
            options:vhost-server-path=/tmp/vhost-server1

# Define and start VMs
virsh define dpdk-vm1-server.xml
virsh define dpdk-vm2-client.xml
virsh start dpdk-vm1-server
virsh start dpdk-vm2-client
