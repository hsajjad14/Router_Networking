# CSC358 a2 Router_Networking

## Simple End System
To test the simple end-system which is running on host2:
1. First run `nc -l <port>` on host1
2. On host2 run `python simple_end_sys/server_client/server.py <port> <host1's ip> <ttl> <file_path_to_send>` This sends a file to host1 then listens to any message and it recieves on \<port\> and prints it. Here we can verify that on host1 the file we sent from host2 appears, now host2 listens to messages and prints anything it recieves
3. On host1 run `python simple_end_sys/server_client/client.py <port> <host2's ip> <file_path_to_send>`. This sends a file to host2 end-system which prints it.
