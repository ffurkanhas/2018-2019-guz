package UDPStopAndWait;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.net.*;
import java.nio.ByteBuffer;

class UDPStopAndWaitSender {
	private static final int BUFFER_SIZE = 1024;
	private static final int PORT = 6789;
	private static final String HOSTNAME = "localhost";
	private static final String SPLITTER = "#-#:#-#";
	private static final String fileName = "deneme.txt";
	private static final int MAGICNUMBER = 16079;

	public static void main(String args[]) throws Exception {
		InetAddress IPAddress = InetAddress.getByName("localhost");
		DatagramSocket socket = new DatagramSocket();

		byte[] sendData;
		byte[] receiveData;

		File sendedFile = new File(fileName); //TODO: change as args[1]
		FileInputStream fis = new FileInputStream(sendedFile);
		BufferedInputStream bis = new BufferedInputStream(fis);

		int fileLength = (int) sendedFile.length();
		int seqFlag = 1;

		String connectionMessage = "--connectedSender--";
		sendData = connectionMessage.getBytes();
		DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, PORT);
		socket.send(sendPacket);
		int ackSeqNumber = 0;
		int totalRead = 0;
		byte[] fileContent = new byte[1024];
		socket.setSoTimeout(10000);
		while (true){
			try {
				while (seqFlag <= (fileLength / 962)+ 2) {
					int willRead = 0;
					boolean lastFlag = false;
					if((seqFlag) * 962 <= fileLength){
						willRead = 962;
						totalRead += 962;
					}
					else{
						lastFlag = true;
						willRead = fileLength - totalRead;
						totalRead += willRead;
					}
					System.out.println("Total Read: " + totalRead + " File Length: " + fileLength);
					fileContent = new byte[willRead];
					bis.read(fileContent, 0, willRead);
					ByteBuffer byteBuffer = ByteBuffer.allocate(32 + 7 + 16 + 7 + willRead); //4: seqNumber, 32: checksum

					String bin = "";
					if(!lastFlag)
						bin = Integer.toBinaryString(0x10000 | seqFlag).substring(1);
					else{
						bin = Integer.toBinaryString(0x10000 | MAGICNUMBER).substring(1);
						System.out.println("magic number sent " + bin);
					}

					Packet filePart = new Packet(fileContent, bin);

					byteBuffer.put(filePart.checksum.getBytes());
					byteBuffer.put(SPLITTER.getBytes());
					byteBuffer.put(filePart.sequenceNumber.getBytes());
					byteBuffer.put(SPLITTER.getBytes());
					byteBuffer.put(filePart.content);

					// Create a byte array for sending and receiving data
					receiveData = new byte[BUFFER_SIZE];
					sendData = new byte[32 + 7 + 16 + 7 + willRead];

					sendData = byteBuffer.array();
					// Send the UDP Packet to the server
					DatagramPacket packet = new DatagramPacket(sendData, sendData.length, IPAddress, PORT);
					System.out.println("packet lentgh: " + packet.getLength());
					socket.send(packet);

					DatagramPacket received = new DatagramPacket(receiveData, receiveData.length);
					socket.receive(received);

					// Get the message from the server's packet
					String returnMessage = new String( received.getData(),0, received.getLength());

					ackSeqNumber = Integer.parseInt(returnMessage, 2);

					if(ackSeqNumber == seqFlag) {
						System.out.println("seqNumber: " + seqFlag +" ack: " + ackSeqNumber + " length: " + filePart.content.length);
						seqFlag++;
					}
					else if(ackSeqNumber == MAGICNUMBER){
						System.out.println("seqNumber: " + seqFlag +" ack: " + ackSeqNumber + " length: " + filePart.content.length);
						break;
					}
					else{
						totalRead -= 962;
						System.out.println("**seqNumber: " + seqFlag +" ack: " + ackSeqNumber + " length: " + filePart.content.length);
					}

				}
			} catch (SocketTimeoutException e){
				seqFlag--;
			}
			break;
		}

		System.out.println("bitti");
	}
}

class Packet{
	String checksum;
	String sequenceNumber;
	byte[] content;

	public Packet(byte[] content, String sequenceNumber){
		this.checksum = org.apache.commons.codec.digest.DigestUtils.md5Hex(content);
		this.sequenceNumber = sequenceNumber;
		this.content = content;
//		String printMessage = String.format("Seq number: %s Checksum: %s", sequenceNumber, this.checksum);
//		System.out.println(printMessage);
	}
}