import sys
import dns.resolver
import threading
import socket
import datetime
from queue import Queue

def resolveDns(hostnames,lookupFail,lookupSuccess):
  for host in hostnames:
    try: 
      host = host.split(",")[1]
      answers = dns.resolver.resolve(host, 'A')
      # Currently writing list of ips to the output file after doing DNS resolution
      for rec in answers:
        lookupSuccess.put(f"{rec}")        
    except Exception as e:
      lookupFail.put(f"{host}, {e}")


if __name__ == "__main__":
  try: 
    lookupFail = Queue(maxsize=0)
    lookupSuccess = Queue(maxsize=0)

    filename = "../Umbrella/top1m/{}.csv".format(sys.argv[1])

    with open(filename) as file:
      hostnames = file.readlines()
      hostnames = [line.rstrip() for line in hostnames]

    start = datetime.datetime.now()
    
    threads = list()

    chunksize = 10000
    
    chunks = [hostnames[i:i + chunksize] for i in range(0, len(hostnames), chunksize)]

    for chunk in chunks:
      x = threading.Thread(target=resolveDns, args=(chunk,lookupFail,lookupSuccess))
      threads.append(x)
      x.start()

    for chunk, thread in enumerate(threads):
      thread.join()

    end = datetime.datetime.now()
    duration = end - start
    totalFails = lookupFail.qsize()
    totalSuccesses = lookupSuccess.qsize()
    ip_list = list(lookupSuccess.queue)
    output = open("../Umbrella/DNS/{}.csv".format(sys.argv[1]), "w")
    output.writelines(line + '\n' for line in ip_list)
    output.close()

    print(" ")
    print(f"Time taken: {duration}")
    print(f"Successfully resolved: {totalSuccesses}")
    print(f"DNS Resolution errors: {totalFails}")
    print(" ")
  except KeyboardInterrupt: 
    ip_list = list(lookupSuccess.queue)
    output = open("../Umbrella/DNS/{}.csv".format(sys.argv[1]), "w")
    output.writelines(line + '\n' for line in ip_list)
    output.close()