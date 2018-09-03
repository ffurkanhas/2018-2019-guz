package TCP;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;
import java.util.ArrayList;

class ServerClientThread extends Thread {
    private Socket serverClient;
    private int clientNo;

    public static ArrayList<Socket> clientSocketList = new ArrayList<>();

    ServerClientThread(Socket inSocket,int counter){
        serverClient = inSocket;
        clientNo = counter;
    }

    public void run(){
        try{
            while (clientSocketList.size() < 2){
                //wait sender and receiver until connected
            }
            System.out.println("all clients connected");
            DataInputStream inStreamSender = new DataInputStream(clientSocketList.get(0).getInputStream());
            DataOutputStream outStreamSender = new DataOutputStream(clientSocketList.get(0).getOutputStream());
            DataInputStream inStreamReceiver = new DataInputStream(clientSocketList.get(1).getInputStream());
            DataOutputStream outStreamReceiver = new DataOutputStream(clientSocketList.get(1).getOutputStream());

            outStreamSender.writeUTF("--connected--");
            outStreamSender.flush();

            outStreamReceiver.writeUTF("--connected--");
            outStreamReceiver.flush();

            byte[] contents;

            long fileLength = Long.parseLong(inStreamSender.readUTF());
            System.out.println(fileLength + " will receive and send");

            outStreamReceiver.writeUTF(String.valueOf(fileLength));
            outStreamReceiver.flush();

            long current = 0;

            while(current < fileLength) {
                int size = 1024;
                if (fileLength - current >= size)
                    current += size;
                else {
                    size = (int) (fileLength - current);
                    current = fileLength;
                }
                contents = new byte[size];
                inStreamSender.read(contents, 0, size);
                outStreamReceiver.write(contents);
                outStreamReceiver.flush();
                System.out.println("Downloading file and uploading ... " + (current * 100) / fileLength + "% complete! " + "Remaining size: " + (fileLength - current));
            }

            String sendersHash = inStreamSender.readUTF();
            System.out.println("Sender's hash :" + sendersHash);
            outStreamReceiver.writeUTF(sendersHash);

            inStreamSender.close();
            outStreamSender.close();
            inStreamReceiver.close();
            outStreamReceiver.close();
            serverClient.close();
        } catch(Exception ex){
            System.out.println(ex);
        } finally{
            System.out.println("Client - " + clientNo + " exit!! ");
        }
    }
}
