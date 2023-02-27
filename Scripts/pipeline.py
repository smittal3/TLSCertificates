import os
import filecmp
import subprocess
from subprocess import Popen, PIPE
from datetime import date, timedelta, datetime

# Connect whole repo to a github repo for backup
def initiate_pipeline(log):
  start = datetime.now()
  os.system("touch ../logs/started.txt")
  yesterday = date.today() - timedelta(days = 1)
  dayBefore = date.today() - timedelta(days = 2)
  yesterday = datetime.strftime(yesterday, '%m_%d_%y')
  
  # Get the files
  log.write("Date: " + yesterday + " \n DateTime: " + str(start) +  "\n\n")
  log.write("EVENT: Getting Data\n")
  process = subprocess.run(['./getData.sh'], stdout=PIPE, stderr=PIPE)
  log.write("Stdout: \n")
  log.write(process.stdout.decode("utf-8") + "\n")
  log.write("Stderr: \n")
  log.write(process.stderr.decode('utf-8') + "\n")

  # Check to see if data is different from previous day
  # Majestic
  try: 
    log.write("EVENT: Majestic Data change since yesterday\n")
    if(filecmp("../Majestic/{}.csv".format(yesterday), "../Majestic/{}.csv".format(dayBefore))):
      log.write("False\n")
    else:
      log.write("True\n")
  except: 
      log.write("A FILE IS MISSING\n")
      
  # Cisco
  try: 
    log.write("EVENT: Cisco Data change since yesterday\n")
    if(filecmp("../Umbrella/{}.csv".format(yesterday), "../Umbrella/{}.csv".format(dayBefore))):
      log.write("False\n")
    else:
      log.write("True\n")
  except: 
      log.write("A FILE IS MISSING\n")


  # Do DNS resolution on both datasets and get IPs
  log.write("\nEVENT: Cisco Umbrella DNS\n")
  process2 = subprocess.run(['python3', 'resolveCisco.py', yesterday], stdout=PIPE, stderr=PIPE)
  log.write("Stdout: \n")
  log.write(process2.stdout.decode("utf-8") + "\n")
  log.write("Stderr: \n")
  log.write(process2.stderr.decode('utf-8') + "\n")
  
  log.write("\nEVENT: Majestic DNS\n")
  process3 = subprocess.run(['python3', 'resolveMajestic.py', yesterday], stdout=PIPE, stderr=PIPE)
  log.write("Stdout: \n")
  log.write(process3.stdout.decode("utf-8") + "\n")
  log.write("Stderr: \n")
  log.write(process3.stderr.decode('utf-8') + "\n")
  

  # Run Zmap on both IP lists to get reduced IP list 
  # Need to modify zmap Bandwith option
  log.write("\nEVENT: Cisco Umbrella Zmap\n")
  process4 = subprocess.run(['zmap', "-B" , "20M", '-p', '443', "-o", "../Umbrella/Zmap/{}.csv".format(yesterday), '--whitelist-file=../Umbrella/DNS/{}.csv'.format(yesterday)], stdout=PIPE, stderr=PIPE)
  log.write("Stdout: \n")
  log.write(process4.stdout.decode("utf-8") + "\n")
  log.write("Stderr: \n")
  log.write(process4.stderr.decode('utf-8') + "\n")
  
  log.write("\nEVENT: Majestic Zmap\n")
  process5 = subprocess.run(['zmap', "-B" , "20M", '-p', '443', "-o", "../Majestic/Zmap/{}.csv".format(yesterday), '--whitelist-file=../Majestic/DNS/{}.csv'.format(yesterday)], stdout=PIPE, stderr=PIPE)
  log.write("Stdout: \n")
  log.write(process5.stdout.decode("utf-8") + "\n")
  log.write("Stderr: \n")
  log.write(process5.stderr.decode('utf-8') + "\n")


  # Run ZGrab on both zmap lists to get cert chains
  log.write("\nEVENT: Cisco Umbrella Zgrab\n")
  process6 = subprocess.run(['/home/ubuntu/go/src/github.com/zmap/zgrab2/zgrab2', "--port" , "443", '--tls', '--output-file=../Umbrella/Zgrab/{}.json'.format(yesterday), "--input-file=../Umbrella/Zmap/{}.csv".format(yesterday)], stdout=PIPE, stderr=PIPE)
  log.write("Stdout: \n")
  log.write(process6.stdout.decode("utf-8") + "\n")
  log.write("Stderr: \n")
  log.write(process6.stderr.decode('utf-8') + "\n")
  
  log.write("\nEVENT: Majestic Zgrab\n")
  process7 = subprocess.run(['/home/ubuntu/go/src/github.com/zmap/zgrab2/zgrab2', "--port" , "443", '--tls', '--output-file=../Majestic/Zgrab/{}.json'.format(yesterday), "--input-file=../Majestic/Zmap/{}.csv".format(yesterday)], stdout=PIPE, stderr=PIPE)
  log.write("Stdout: \n")
  log.write(process7.stdout.decode("utf-8") + "\n")
  log.write("Stderr: \n")
  log.write(process7.stderr.decode('utf-8') + "\n")
  
  end = datetime.now()
  duration = end - start
  log.write("\nDaily Scan Complete at: " + str(end) + " \n Duration: " + str(duration) + "\n")

  log.close()
  

if __name__ == "__main__":
  try:
    yesterday = date.today() - timedelta(days = 1)
    yesterday = datetime.strftime(yesterday, '%m_%d_%y')
    log = open("../logs/" + yesterday + ".txt", "w")
    initiate_pipeline(log)
  except KeyboardInterrupt:
    log.close()
