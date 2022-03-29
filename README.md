# CSC358 a2 Router_Networking

## Simple End System
To test the simple end-system which is running on host2:
1. First run `nc -l <port>` on host1
2. On host2 run `python simple_end_sys/server_client/server.py <port> True True <host1's ip> <ttl> <file_path_to_send>` This:
    * Sets the flag for broadcasting host2 to the router
    * Sets the flag to send a message
    * Sends the specified file to host1 
    * ... Then listens to any message it recieves on \<port\> and prints it. Here we can verify that on host1 the file we sent from host2 appears, now host2 listens to messages and prints anything it recieves
4. On host1 run `python simple_end_sys/server_client/client.py <port> <host2's ip> <ttl> <file_path_to_send>`. This sends a file (given the TTL is sufficiently large) to host2 end-system which prints it.


## Simple Router
1. cd into simple_router directory
2. Run sudo mn -x --custom custom_topo2.py --topo mytopo
3. In the terminal window for r1 run `./scripts_for_router`
4. To test:
5. on h1 and h4 run ifconfig (h1's ip = 10.0.1.10, h4's ip = 10.0.2.20)
6. On h4 use netcat to open the port on h4: `nc -l 5678`
7. On h1 use netcat to send a message to h4 nc 10.0.2.20 5678 < test_snd 
8. (test_snd is a file with text in it)
9. Verify the message was sent


## Multi Net Router
1. Run `sudo python multi_net_OSPF.py`
