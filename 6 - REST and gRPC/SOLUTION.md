
|  Method 	| Local  	| Same-Zone  	|  Different Region 	|
|---	|---	|---	|---	|---	|
|   REST add	|   	|   	|  	|
|   gRPC add	|   	|   	|    	|
|   REST img	|   	|   	|   	|
|   gRPC img	|       |   	|   	|
|   PING        |       |      |       |

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.