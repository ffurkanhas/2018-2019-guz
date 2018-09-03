package UDPStopAndWait;

import java.io.*;
import java.net.*;

class UDPStopAndWaitServer{
    private static final int PORTSENDER = 6789;
    private static final int PORTRECEIVER = 6790;
    private static int senderPort, receiverPort;
    private static DatagramSocket clientSenderSocket;
    private static DatagramSocket clientReceiverSocket;
    private static InetAddress IPAddress;
    private static double errorRate;
    private static boolean errorRateFlag = true;

    public static void main(String[] args) throws IOException {
        IPAddress = InetAddress.getByName("localhost");
        clientSenderSocket = new DatagramSocket(PORTSENDER);
        clientReceiverSocket = new DatagramSocket(PORTRECEIVER);

        if(errorRateFlag){
            File file = new File("pAndQFile.txt");

            BufferedReader br = new BufferedReader(new FileReader(file));

            double p = Double.parseDouble(br.readLine().replace(",", "."));
            double q = Double.parseDouble(br.readLine().replace(",", "."));

            errorRate = p - q;
        }

        setUpConnections();

        forwardDatas();
    }

    private static void forwardDatas() throws IOException {
        byte[] receiveData = new byte[1024];
        int i = 0;
        while(true){
            i++;
            /*
             Get data from client 1 and forward to client 2
            */
            DatagramPacket receivedForSender = new DatagramPacket( receiveData, receiveData.length );
            clientSenderSocket.receive( receivedForSender );

            // Get the message from the packet
            String message = new String( receivedForSender.getData(),0, receivedForSender.getLength());

            // Send the packet data to client 2
            DatagramPacket packet;
            if(errorRateFlag){
                double randomNumber = Math.random();
                if(errorRate < randomNumber){
                    System.out.println("error");
                    byte[] deneme = message.getBytes();
                    for(int j = 63; j < deneme.length; j++){
                        byte temp = deneme[j];
                        temp = (byte) (temp | (1 << 3));
                        deneme[j] = temp;
                    }
                    String tempString = new String(deneme, 0, deneme.length);
                    packet = new DatagramPacket( tempString.getBytes(), tempString.getBytes().length, IPAddress, receiverPort );
                    clientReceiverSocket.send( packet );
                }
                else {
                    packet = new DatagramPacket( message.getBytes(), message.getBytes().length, IPAddress, receiverPort );
                    clientReceiverSocket.send( packet );
                }
            }
            else{
                packet = new DatagramPacket( message.getBytes(), message.getBytes().length, IPAddress, receiverPort );
                clientReceiverSocket.send( packet );
            }

            /*
             Get data from client 2 and forward to client 1
            */
            receivedForSender = new DatagramPacket( receiveData, receiveData.length );
            clientReceiverSocket.receive( receivedForSender );

            // Get the message from the packet
            message = new String( receivedForSender.getData(),0, receivedForSender.getLength());

            // Send the packet data to client 1
            packet = new DatagramPacket( message.getBytes(), message.getBytes().length, IPAddress, senderPort );
            clientSenderSocket.send( packet );
        }
    }

    private static void setUpConnections() throws IOException {
        byte[] receiveData = new byte[1024];

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
    }
}