# Create bridge
sudo brctl addbr br0
sudo ip link set br0 up

# Define and start VMs
virsh define bridge-vm1-server.xml
virsh define bridge-vm2-client.xml
virsh start bridge-vm1-server
virsh start bridge-vm2-client
