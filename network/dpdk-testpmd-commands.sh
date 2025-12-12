sudo dpdk-testpmd -l 0-15 -n 8   -- --nb-cores=4 --rxq=8 --txq=8 --forward-mode=rxonly --nb-cores=8 --stats-period=1
sudo dpdk-testpmd -l 0-15 -n 8   -- --nb-cores=4 --rxq=8 --txq=8 --nb-cores=8 -i

