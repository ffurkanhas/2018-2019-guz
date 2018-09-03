package UDPStopAndWait;

import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import java.nio.charset.StandardCharsets;

public class UDPStopAndWaitReceiver {
    private static final int BUFFER_SIZE = 1024;
    private static final int PORT = 6790;
    private static final String HOSTNAME = "localhost";
    private static final String SPLITTER = "#-#:#-#";
    private static final int MAGICNUMBER = 16079;

    public static void main(String args[]) throws Exception {
        long downloadStartTime = System.currentTimeMillis();
        InetAddress IPAddress = InetAddress.getByName("localhost");
        // Create a socket
        DatagramSocket socket = new DatagramSocket();

        byte[] sendData = new byte[1024];
        byte[] receiveData = new byte[1024];

        String connectionMessage = "--connectedReceiver--";
        sendData = connectionMessage.getBytes();
        DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, PORT);
        socket.send(sendPacket);

        String filePath = "gelen.txt"; //TODO: change as args[1]

        FileOutputStream fos = new FileOutputStream(filePath);
        BufferedOutputStream bos = new BufferedOutputStream(fos);

        socket.setSoTimeout(1000);
        String givenSeqNumberString = "";
        int retryPackageLoss = 0;
        int retryCheckSumError = 0;
        int fileLength = 0;
        while (true)  {
            try {
                // Create a byte array for sending and receiving data
                receiveData = new byte[BUFFER_SIZE];

                // Receive the server's packet
                DatagramPacket received = new DatagramPacket(receiveData, receiveData.length);
                socket.receive(received);

                String message = new String( received.getData(),0, received.getLength());

                byte[] tempData = new byte[received.getLength()];
                System.arraycopy(received.getData(), received.getOffset(), tempData, 0, received.getLength());

                String allDataString = new String(tempData, StandardCharsets.UTF_8);
                String[] infos = allDataString.split(SPLITTER);
                String givenCheckSum = infos[0];
                givenSeqNumberString = infos[1];
                int givenSeqnumber = Integer.parseInt(givenSeqNumberString, 2);
                String givenData = infos[2];

                fileLength += givenData.length();

                System.out.println(givenCheckSum + " " + givenSeqnumber + " length: " + givenData.getBytes().length + " Readed file legth: " + fileLength);

                byte[] givenDataBytes = givenData.getBytes();

                String calculatedCheckSum = org.apache.commons.codec.digest.DigestUtils.md5Hex(givenDataBytes);

                System.out.println("calculated checksum: " + calculatedCheckSum);

                if(calculatedCheckSum.equals(givenCheckSum)){
                    if(givenSeqnumber != MAGICNUMBER){
                        bos.write(givenDataBytes);
                        sendData = givenSeqNumberString.getBytes();
                        DatagramPacket packet = new DatagramPacket(sendData, sendData.length, IPAddress, PORT);
                        socket.send(packet);
                    }
                    else{
                        System.out.println("son");
                        bos.write(givenDataBytes);
                        sendData = givenSeqNumberString.getBytes();
                        DatagramPacket packet = new DatagramPacket(sendData, sendData.length, IPAddress, PORT);
                        socket.send(packet);
                        break;
                    }
                    retryCheckSumError = 0;
                    retryPackageLoss = 0;
                }
                else{
                    System.out.println("checksum esit degil");
                    if(retryCheckSumError < 5){
                        System.out.println("tekrar");
                        retryCheckSumError++;
                        givenSeqnumber--;
                        givenSeqNumberString = Integer.toBinaryString(0x10000 | givenSeqnumber).substring(1);
                        sendData = givenSeqNumberString.getBytes();
                        DatagramPacket packet = new DatagramPacket(sendData, sendData.length, IPAddress, PORT);
                        socket.send(packet);
                    }
                    else{
                        givenSeqnumber++;
                        System.out.println("Packet retry limit overhead: send ++givenSeqnumber");
                        givenSeqNumberString = Integer.toBinaryString(0x10000 | givenSeqnumber).substring(1);
                        sendData = givenSeqNumberString.getBytes();
                        DatagramPacket packet = new DatagramPacket(sendData, sendData.length, IPAddress, PORT);
                        socket.send(packet);
                    }
                }

                // Send the UDP Packet to the server

            }catch (SocketTimeoutException e){
                if(retryPackageLoss < 5){
                    retryPackageLoss++;
                    int givenSeqnumber = Integer.parseInt(givenSeqNumberString, 2);
                    System.out.println("Time Out, retry: " + retryPackageLoss + " resend ack:" + givenSeqnumber);
                    sendData = givenSeqNumberString.getBytes();
                    DatagramPacket packet = new DatagramPacket(sendData, sendData.length, IPAddress, PORT);
                    socket.send(packet);
                }
                else {
                    int givenSeqnumber = Integer.parseInt(givenSeqNumberString, 2);
                    System.out.println("Time Out, retry: " + retryPackageLoss + " resend ack:" + givenSeqnumber);
                    givenSeqNumberString = Integer.toBinaryString(0x10000 | givenSeqnumber).substring(1);
                    sendData = givenSeqNumberString.getBytes();
                    DatagramPacket packet = new DatagramPacket(sendData, sendData.length, IPAddress, PORT);
                    socket.send(packet);
                }
            }
        }

        bos.close();
        long downloadEndTime = System.currentTimeMillis();
        long totalTime = downloadEndTime - downloadStartTime;
        System.out.println("Total download time: " + totalTime + "ms");
    }

}
