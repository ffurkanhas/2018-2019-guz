package TCP;

import java.net.*;
import java.io.*;

public class TCPClientReceiver {

    static String serverAddress = "127.0.0.1";
    static int serverPort = 23626;

    public static void main(String[] args){
        try {
            long downloadStartTime = System.currentTimeMillis();
            Socket socket=new Socket(serverAddress,serverPort);
            DataInputStream inStream=new DataInputStream(socket.getInputStream());
            DataOutputStream outStream=new DataOutputStream(socket.getOutputStream());

            String serverMessage = "";

            serverMessage = inStream.readUTF();
            while (!serverMessage.contains("--connected--")) {
                serverMessage = inStream.readUTF();
            }

            long fileLength = Long.parseLong(inStream.readUTF());
            System.out.println(fileLength + " will receive");

            long current = 0;

            byte[] contents;

            String filePath = "gelen.txt"; //TODO: change as args[1]

            //Initialize the FileOutputStream to the output file's full path.
            FileOutputStream fos = new FileOutputStream(filePath);
            BufferedOutputStream bos = new BufferedOutputStream(fos);

            System.out.println("Download starting...");

            int total = 0;
            while(current < fileLength) {
                int size = 1024;
                if (fileLength - current >= size)
                    current += size;
                else {
                    size = (int) (fileLength - current);
                    current = fileLength;
                }
                contents = new byte[size];
                inStream.read(contents, 0, size);
                bos.write(contents, 0, size);
                total += size;
                System.out.println("Downloading file ... " + (current * 100) / fileLength + "% complete! " + "Remaining size: " + (fileLength - current) + " Total: " + total);
            }
            bos.close();
            long downloadEndTime = System.currentTimeMillis();
            long totalTime = downloadEndTime - downloadStartTime;
            System.out.println("Total download time: " + totalTime + "ms");

            FileInputStream fisForMd5 = new FileInputStream(new File(filePath));
            String md5 = org.apache.commons.codec.digest.DigestUtils.md5Hex(fisForMd5);
            fisForMd5.close();

            String sendersHash = inStream.readUTF();
            System.out.println("Sender's hash :" + sendersHash);

            System.out.println(md5);

            inStream.close();
            outStream.close();
            socket.close();
        }catch(Exception e){
            System.out.println(e);
        }
    }
}
