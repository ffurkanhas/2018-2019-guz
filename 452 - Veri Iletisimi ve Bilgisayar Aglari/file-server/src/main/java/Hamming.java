public class Hamming
{
  public static void main(String[] args)
  {
    int[] data = new int[8];             // get bit to send as the first
    for (int i=0; i<8; i++)              // command line parameter
      data[i] = (args[0].charAt(i) == '0') ? 0 : 1;
    System.out.println("Byte to send:");
    printArray(data);

    int[] encodedData = encodeHamming(data);   // encode data with Hamming code
    System.out.println("Encoded data:");
    printArray(encodedData);                   // print the encoded array

    int errorBit = Integer.parseInt(args[1]);            // get error bit number

    if (0 < errorBit && errorBit <= encodedData.length)  // flip the error bit
    {                                                    // in encoded data 
      System.out.println("Flipping bit " + errorBit);
      encodedData[errorBit-1] = 1 - encodedData[errorBit-1]; 
    }
    System.out.println("Received from channel:");
    printArray(encodedData);                  // print corrupted array

    int index = decodeHamming(encodedData);   // apply the Hamming decoding    
    if (index != 0)                           // check for a transmission error
      System.out.println("Transmission error in bit " + index);
    System.out.println("Received from decoder:");
    printArray(encodedData);

    int[] receivedData  = restore(encodedData);   // retrieve the byte sent
    System.out.println("Extracted data:");
    printArray(receivedData);
  }

// this method encodes a byte with a 12-bit string to be send
  public static int[] encodeHamming(int[] a)
  {
    int[] h = new int[12];
    h[0] = (a[0] + a[1] + a[3] + a[4] + a[6]) % 2;
    h[1] = (a[0] + a[2] + a[3] + a[5] + a[6]) % 2;
    h[2] = a[0];
    h[3] = (a[1] + a[2] + a[3] + a[7]) % 2;
    h[4] = a[1];
    h[5] = a[2];
    h[6] = a[3];
    h[7] = (a[4] + a[5] + a[6] + a[7]) % 2;
    h[8] = a[4];
    h[9] = a[5];
    h[10] = a[6];
    h[11] = a[7];
    return(h); 
  }

// this method checks for a transmission error and corrects the data
  public static int decodeHamming(int[] a)
  {
    int[] p = new int[4];
    p[0] = (a[0] + a[2] + a[4] + a[6] + a[8] + a[10]) % 2;
    p[1] = (a[1] + a[2] + a[5] + a[6] + a[9] + a[10]) % 2;
    p[2] = (a[3] + a[4] + a[5] + a[6] + a[11]) % 2;
    p[3] = (a[7] + a[8] + a[9] + a[10] + a[11]) % 2;
    int index = 8*p[3] + 4*p[2] + 2*p[1] + p[0];
    if (index != 0)
      a[index-1] = 1 - a[index-1];            // error correction
    return (8*p[3] + 4*p[2] + 2*p[1] + p[0]);
  }

// this method extracts 8-bit data from the received 12-bit string
  public static int[] restore(int[] a)
  {
    int[] b = {a[2], a[4], a[5], a[6], a[8], a[9], a[10], a[11]}; 
    return(b);
  }

// this method prints a bit string
  public static void printArray(int[] a)
  {
    for (int i=0; i<a.length; i++)
      System.out.print(a[i]);
    System.out.println();
  }
}