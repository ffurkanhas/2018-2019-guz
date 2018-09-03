package UDP;

import java.io.*;
import java.net.*;

class UDPClientSender {
   public static void main(String args[]) throws Exception {
      long uploadStartTime = System.currentTimeMillis();
      DatagramSocket clientSocket = new DatagramSocket();
      InetAddress IPAddress = InetAddress.getByName("localhost");

      byte[] sendData = new byte[1024];
      byte[] receiveData = new byte[1024];

      String connectionMessage = "--connectedSender--";
      sendData = connectionMessage.getBytes();
      DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 9876);
      clientSocket.send(sendPacket);

      String filePath = "deneme.txt";

      File sendedFile = new File(filePath); //TODO: change as args[1]
      FileInputStream fis = new FileInputStream(sendedFile);
      BufferedInputStream bis = new BufferedInputStream(fis);

      DatagramPacket serverConnectionResponse = new DatagramPacket(receiveData, receiveData.length);
      clientSocket.receive(serverConnectionResponse);
      String sentenceSender = new String( serverConnectionResponse.getData(),0, serverConnectionResponse.getLength());

      while(!sentenceSender.contains("--established--")){
         clientSocket.receive(serverConnectionResponse);
         sentenceSender = new String( serverConnectionResponse.getData(),0, serverConnectionResponse.getLength());
      }

      FileInputStream fisForMd5 = new FileInputStream(new File(filePath));
      String md5 = org.apache.commons.codec.digest.DigestUtils.md5Hex(fisForMd5);
      fisForMd5.close();

      System.out.println(md5);

      byte[] sumOfFile = md5.getBytes();
      DatagramPacket sumOfFilePacket = new DatagramPacket(sumOfFile, sumOfFile.length, IPAddress, 9876);
      clientSocket.send(sumOfFilePacket);

      long fileLength = sendedFile.length();
      long current = 0;
      byte[] contents;

      while(current < fileLength) {
         int size = 1024;
         if (fileLength - current >= size)
            current += size;
         else {
            size = (int) (fileLength - current);
            current = fileLength;
         }
         contents = new byte[size];
         bis.read(contents, 0, size);
         DatagramPacket filePart = new DatagramPacket(contents, contents.length, IPAddress, 9876);
         clientSocket.send(filePart);
         System.out.println("Sending file ... " + (current * 100) / fileLength + "% complete! " + "Remaining size: " + (fileLength - current));
      }

      String endOfFile = "-#ENDOFFILE#-";
      byte[] endOfFileByte = endOfFile.getBytes();
      DatagramPacket endOfFilePacket = new DatagramPacket(endOfFileByte, endOfFileByte.length, IPAddress, 9876);

      clientSocket.send(endOfFilePacket);

      long uploadEndTime = System.currentTimeMillis();
      long totalTime = uploadEndTime - uploadStartTime;
      System.out.println("Total download time: " + totalTime + "ms");

      clientSocket.close();
   }
}