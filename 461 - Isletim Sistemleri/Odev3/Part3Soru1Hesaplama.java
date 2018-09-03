package com.naneb;

import java.util.Scanner;

public class Part3Soru1Hesaplama {

    public static void main(String[] args) {

        Scanner kyb = new Scanner(System.in);

        int baseAddress = 128;

        int baseSize = 512;

        String baseAddressBinary = Integer.toBinaryString(baseAddress);

        while(true){
            int address = kyb.nextInt();

            if(address == -1607){
                break;
            }

            String binaryAddress;

            binaryAddress = String.format("%07d", Integer.valueOf(Integer.toBinaryString(address)));

            int segmentNumber = Integer.parseInt(binaryAddress.substring(0,1));

            int maxSegment = (int) Math.pow(2, (7 - segmentNumber));

            String binaryAddressWithoutSegment = binaryAddress.substring(1);

            int offSet;

            if(segmentNumber == 1){
                offSet = Integer.parseInt(binaryAddressWithoutSegment, 2) - maxSegment;
            }
            else {
                offSet = address;
            }

            int physicalAddress = baseSize + offSet;

            System.out.println("Binary address: " + binaryAddress);
            System.out.println("Binary address without segment number: " + binaryAddressWithoutSegment);
            System.out.println("Segment number: " + segmentNumber);

            if(Math.abs(offSet) <= 20 ){
                System.out.println("Answer is: Valid in Segment " + segmentNumber);
            }
            else{
                System.out.println("Answer is: not valid in Segment " + segmentNumber);
            }

        }

    }
}
