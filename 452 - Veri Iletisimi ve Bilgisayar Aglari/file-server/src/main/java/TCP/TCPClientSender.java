package TCP;

import java.net.*;
import java.io.*;

public class TCPClientSender {

    public static void main(String[] args){
        try {
            long uploadStartTime = System.currentTimeMillis();
            String serverAddress = "127.0.0.1";
            int serverPort = 23626;

            Socket socket=new Socket(serverAddress, serverPort);
            DataInputStream inStream=new DataInputStream(socket.getInputStream());
            DataOutputStream outStream=new DataOutputStream(socket.getOutputStream());
            String serverMessage = "";

            serverMessage = inStream.readUTF();
            while (!serverMessage.contains("--connected--")) {
                serverMessage = inStream.readUTF();
            }

            String filePath = "deneme.txt";

            File sendedFile = new File(filePath); //TODO: change as args[1]
            FileInputStream fis = new FileInputStream(sendedFile);
            BufferedInputStream bis = new BufferedInputStream(fis);

            long fileLength = sendedFile.length();
            long current = 0;
            byte[] contents;

            System.out.println(fileLength);

            outStream.writeUTF(String.valueOf(fileLength));
            outStream.flush();

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
                outStream.write(contents);
                outStream.flush();
                System.out.println("Sending file ... " + (current * 100) / fileLength + "% complete! " + "Remaining size: " + (fileLength - current));
            }
            long uploadEndTime = System.currentTimeMillis();
            long totalTime = uploadEndTime - uploadStartTime;
            System.out.println("Total upload time: " + totalTime + "ms");

            FileInputStream fisForMd5 = new FileInputStream(new File(filePath));
            String md5 = org.apache.commons.codec.digest.DigestUtils.md5Hex(fisForMd5);
            fisForMd5.close();

            System.out.println(md5);
            outStream.writeUTF(md5);

            inStream.close();
            outStream.close();
            socket.close();
        } catch(Exception e){
          System.out.println(e);
        }
    }
}
