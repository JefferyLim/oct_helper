# Create VLAN interfaces on the physical NIC (adjust ens1f0)
sudo ip link add link ens1f0 name ens1f0.100 type vlan id 100
sudo ip link add link ens1f0 name ens1f0.200 type vlan id 200
sudo ip link set ens1f0.100 up
sudo ip link set ens1f0.200 up

# Create separate bridges per VLAN
sudo brctl addbr brvlan100
sudo brctl addbr brvlan200
sudo brctl addif brvlan100 ens1f0.100
sudo brctl addif brvlan200 ens1f0.200
sudo ip link set brvlan100 up
sudo ip link set brvlan200 up

# Configure external switch to route between VLAN 100 and VLAN 200

# Define and start VMs
virsh define hairpin-vm1-server.xml
virsh define hairpin-vm2-client.xml
virsh start hairpin-vm1-server
virsh start hairpin-vm2-client
