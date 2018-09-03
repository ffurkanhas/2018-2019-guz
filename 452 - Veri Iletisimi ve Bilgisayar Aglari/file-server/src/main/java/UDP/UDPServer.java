package UDP;

import java.net.*;

class UDPServer {

    public static void main(String args[]) throws Exception {
        DatagramSocket clientSenderSocket = new DatagramSocket(9876);
        DatagramSocket clientReceiverSocket = new DatagramSocket(9875);
        InetAddress IPAddress = InetAddress.getByName("localhost");
        byte[] receiveData = new byte[1024];
        byte[] sendData;

        int senderPort, receiverPort;

        DatagramPacket receivePacketSender = new DatagramPacket(receiveData, receiveData.length);
        clientSenderSocket.receive(receivePacketSender);
        String sentenceSender = new String( receivePacketSender.getData(),0, receivePacketSender.getLength());

        senderPort = receivePacketSender.getPort();

        System.out.println(sentenceSender + ", sender port: " + senderPort);

        DatagramPacket receivePacketReceiver = new DatagramPacket(receiveData, receiveData.length);
        clientReceiverSocket.receive(receivePacketReceiver);
        String sentenceReceiver = new String( receivePacketReceiver.getData(),0, receivePacketReceiver.getLength());

        receiverPort = receivePacketReceiver.getPort();

        System.out.println(sentenceReceiver + ", sender port: " + receiverPort);

        String connectionMessage = "--established--";
        sendData = connectionMessage.getBytes();
        DatagramPacket sendPacketSender = new DatagramPacket(sendData, sendData.length, IPAddress, senderPort);
        clientSenderSocket.send(sendPacketSender);

        DatagramPacket sendPacketReceiver = new DatagramPacket(sendData, sendData.length, IPAddress, receiverPort);
        clientSenderSocket.send(sendPacketReceiver);

        DatagramPacket hashFromSenderPacket = new DatagramPacket(receiveData, receiveData.length);
        clientSenderSocket.receive(hashFromSenderPacket);

        DatagramPacket hashSentReceiver = new DatagramPacket(hashFromSenderPacket.getData(), hashFromSenderPacket.getLength(), IPAddress, receiverPort);
        clientReceiverSocket.send(hashSentReceiver);

        String hashFromSender = new String( hashFromSenderPacket.getData(),0, hashFromSenderPacket.getLength());
        System.out.println(hashFromSender);

        String sentenceFromSender = "";

        clientSenderSocket.setSoTimeout(500);

        try {
            while (!sentenceFromSender.contains("-#ENDOFFILE#-")){
                DatagramPacket filePart = new DatagramPacket(receiveData, receiveData.length);
                clientSenderSocket.receive(filePart);

                DatagramPacket filePartSent = new DatagramPacket(filePart.getData(), filePart.getLength(), IPAddress, receiverPort);
                clientReceiverSocket.send(filePartSent);

                sentenceFromSender = new String( filePart.getData(),0, filePart.getLength());
            }
        } catch (SocketTimeoutException e){
            e.printStackTrace();
        }


   }
}