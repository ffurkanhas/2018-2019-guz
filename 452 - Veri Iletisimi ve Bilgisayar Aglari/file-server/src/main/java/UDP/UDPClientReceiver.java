package UDP;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.net.*;

class UDPClientReceiver {
    public static void main(String args[]) throws Exception {
        long downloadStartTime = System.currentTimeMillis();
        DatagramSocket clientSocket = new DatagramSocket();
        InetAddress IPAddress = InetAddress.getByName("localhost");

        byte[] sendData = new byte[1024];
        byte[] receiveData = new byte[1024];

        String connectionMessage = "--connectedReceiver--";
        sendData = connectionMessage.getBytes();
        DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 9875);
        clientSocket.send(sendPacket);

        DatagramPacket serverConnectionResponse = new DatagramPacket(receiveData, receiveData.length);
        clientSocket.receive(serverConnectionResponse);
        String sentenceSender = new String( serverConnectionResponse.getData(),0, serverConnectionResponse.getLength());

        while(!sentenceSender.contains("--established--")){
            clientSocket.receive(serverConnectionResponse);
            sentenceSender = new String( serverConnectionResponse.getData(),0, serverConnectionResponse.getLength());
        }

        DatagramPacket hashFromSenderPacket = new DatagramPacket(receiveData, receiveData.length);
        clientSocket.receive(hashFromSenderPacket);

        String hashFromSender = new String( hashFromSenderPacket.getData(),0, hashFromSenderPacket.getLength());

        String sentenceFromSender = "";

        String filePath = "gelen.txt"; //TODO: change as args[1]

        FileOutputStream fos = new FileOutputStream(filePath);
        BufferedOutputStream bos = new BufferedOutputStream(fos);

        clientSocket.setSoTimeout(500);

        try {
            while (!sentenceFromSender.contains("-#ENDOFFILE#-")){
                DatagramPacket filePart = new DatagramPacket(receiveData, receiveData.length);
                clientSocket.receive(filePart);

                bos.write(filePart.getData(), 0, filePart.getLength());
                sentenceFromSender = new String( filePart.getData(),0, filePart.getLength());
            }
        } catch (SocketTimeoutException e){
            e.printStackTrace();
        } finally {
            bos.close();

            long downloadEndTime = System.currentTimeMillis();
            long totalTime = downloadEndTime - downloadStartTime;
            System.out.println("Total download time: " + totalTime + "ms");
            FileInputStream fisForMd5 = new FileInputStream(new File(filePath));
            String md5 = org.apache.commons.codec.digest.DigestUtils.md5Hex(fisForMd5);
            fisForMd5.close();

            System.out.println("Hash from me: " + md5);
            System.out.println("Hash from sender: " + hashFromSender);

            if(hashFromSender.equals(md5))
                System.out.println("File downloaded correctly");
            else
                System.out.println("There is an error");

            clientSocket.close();
        }




    }
}