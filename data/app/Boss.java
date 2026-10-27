import java.io.*;
import java.util.Scanner;

public class Boss {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter a number to process: ");
        String num = input.nextLine();

        try {
            // Java calls the Python Analyst
            Process p = Runtime.getRuntime().exec("python analyst.py " + num);
            BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
            
            String finalResult = in.readLine();
            System.out.println("The final result from the C++/Python/Java chain is: " + finalResult);
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}