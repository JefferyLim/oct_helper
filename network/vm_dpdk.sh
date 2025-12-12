echo 1024 | sudo tee /proc/sys/vm/nr_hugepages
sudo mkdir -p /mnt/huge
sudo mount -t hugetlbfs nodev /mnt/huge


sudo modprobe vfio-pci
echo 1 | sudo tee  /sys/module/vfio/parameters/enable_unsafe_noiommu_mode
sudo dpdk-devbind.py --bind=vfio-pci 0000:00:02.0
