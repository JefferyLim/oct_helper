sudo ip netns add hostns
sudo ip link set enp59s0np1 netns hostns

sudo ip netns exec hostns ip addr add 192.168.40.20/24 dev enp59s0np1
sudo ip netns exec hostns ip link set enp59s0np1 up

sudo ip addr add 192.168.40.10/24 dev enp59s0np0 
sudo ip link set enp59s0np0 up
