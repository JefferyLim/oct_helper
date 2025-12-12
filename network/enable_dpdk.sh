echo 65535 | sudo tee /proc/sys/vm/nr_hugepages
sudo mkdir -p /mnt/huge
sudo mount -t hugetlbfs nodev /mnt/huge

sudo ovs-vsctl set Open_vSwitch . other_config:dpdk-init="true"
sudo ovs-vsctl set Open_vSwitch . other_config:dpdk-socket-mem="4096,4096"
sudo ovs-vsctl set Open_vSwitch . other_config:dpdk-lcore-mask=0xFF00000000
sudo ovs-vsctl set Open_vSwitch . other_config:pmd-cpu-mask=0xFF
