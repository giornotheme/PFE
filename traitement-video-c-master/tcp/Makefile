CC = g++ -std=c++11 -pthread
CFLAGS = -g
OPENCV = `pkg-config opencv4 --cflags --libs`
LIBS = $(OPENCV)

all:
	echo "compiling server..."
	$(CC) $(CFLAGS) -o server server.cpp $(LIBS) -lpthread
	echo "compiling client..."
	$(CC) $(CFLAGS) -o client client.cpp $(LIBS)

client:client.cpp
	$(CC) $(CFLAGS) -o client client.cpp $(LIBS)

server:server.cpp
	$(CC) $(CFLAGS) -o server server.cpp $(LIBS) -lpthread

clean:
	echo "Cleaning ...."
	rm ./client
	rm ./server
