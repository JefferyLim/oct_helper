sudo ovs-vsctl set Open_vSwitch . other_config:dpdk-init="true"
sudo ovs-vsctl set Open_vSwitch . other_config:dpdk-socket-mem="1024,1024"
sudo ovs-vsctl set Open_vSwitch . other_config:dpdk-lcores="16,18,14,20,12,22,10,24"
sudo ovs-vsctl set Open_vSwitch . other_config:pmd-cpu-mask=0x1555400
