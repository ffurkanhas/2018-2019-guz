package TCP;

import java.net.*;

public class FileTransferServer {

    static int serverPort = 23626;

    public static void main(String[] args) throws Exception {
      try {
          ServerSocket server=new ServerSocket(serverPort);
          int counter=0;
          System.out.println("Server Started ....");

          while(true){
              counter++;
              Socket serverClient=server.accept();  //server accept the client connection request
              System.out.println(" >> " + "Client No:" + counter + " started!");
              ServerClientThread sct = new ServerClientThread(serverClient,counter); //send  the request to a separate thread

              ServerClientThread.clientSocketList.add(serverClient);

              sct.start();
          }
      } catch(Exception e){
      System.out.println(e);
      }
    }
}
