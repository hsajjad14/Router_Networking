# CSC358 a2 Router_Networking

## Simple End System
`cd` into `simple_end_sys/server_client`
First, run the mininet topology: `sudo mn --custom custom_topo.py --topo mytopo` and call xterm on any devices as desired in the mininet terminal. To test the simple end-system which is running on h3:
1. First run `nc -lu <port>` on h1 (broadcast implemented using UDP). Also `nc -lu <port>` on r1.
2. On h3 run `python /server.py <port> True False <host1's ip> <ttl> <file_path_to_send>` This:
    * Sets the flag for broadcasting h3 to the router
    * Sets the flag to send a message to false (nobody is listening yet)
    * ... Then listens to any message it recieves on \<port\> and prints it.
4. On h1 run `python simple_end_sys/server_client/client.py <port> <h3's ip> <ttl> <file_path_to_send>`. This sends a file (given the TTL is sufficiently large) to h3 end-system which prints it.


## Simple Router
1. cd into simple_router directory
2. Run sudo mn -x --custom custom_topo2.py --topo mytopo
3. In the terminal window for r1 run `./scripts_for_router`
   * Note: if you encounter the error `/bin/bash^M: bad interpreter: No such file or directory` when running this script, run:
      * `sed -i -e 's/\r$//' scripts_for_router`
      * ./scripts_for_router
5. To test:
6. on h1 and h4 run ifconfig (h1's ip = 10.0.1.10, h4's ip = 10.0.2.20)
7. On h4 use netcat to open the port on h4: `nc -l 5678`
8. On h1 use netcat to send a message to h4: `nc 10.0.2.20 5678 < test_snd` 
9. (test_snd is a file with text in it)
10. Verify the message was sent


## Multi Net Router
In the multi_net_router directory, for topology 1:

![multi_net_topo](https://user-images.githubusercontent.com/40809349/161470161-43b47107-9b32-4b7c-a4fb-9e293b285eb1.png)
1. For OSPF: run `sudo python multi_net_OSPF.py`
2. For RIP: run `sudo python multi_net_RIP.py`

In multi_net_router2 directory, for topology 2:

<img width="449" alt="topo2" src="https://user-images.githubusercontent.com/40809349/161470420-7871e8ec-4856-42ad-b378-d1704119bf56.PNG">

1. For OSPF: run `sudo python multi_net_OSPF2.py`

2. For RIP: run `sudo python multi_net_RIP2.py`


