1. Pull domain list from Cisco Umbrella and Majestic Million
2. For each dataset, check if different from previous day
3. Do domain resolution on both lists
4. Run zmap on both reduced lists
5. Run zgrab on both ip lists and store certs



File structure: 
- Data
  - logs
  - Umbrella
    - top1m
    - DNS
    - zmap
    - zgrab
  - Majestic
    - top1m
    - DNS
    - zmap
    - zgrab
    - logs
  - Scripts




Packages:
1. apt install zmap
2. apt install golang-go
3. go get github.com/zmap/zgrab
4. cd /home/USERNAME/go/src/github.com/zmap/zgrab
5. go build
6. apt install python3 
7. apt install python-pip3
8. pip3 install dnspython