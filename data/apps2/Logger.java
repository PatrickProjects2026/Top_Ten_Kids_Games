import java.io.*;
import java.time.LocalDateTime;

public class Logger {
    public static void main(String[] args) {
        if (args.length == 0)
            return;

        try (FileWriter fw = new FileWriter("bowling_log.txt", true);
                PrintWriter out = new PrintWriter(fw)) {

            String event = args[0];
            out.println(LocalDateTime.now() + " - EVENT: " + event);
            System.out.println("[Java Logger] Recorded: " + event);

        } catch (IOException e) {
            System.err.println("Logger failed: " + e.getMessage());
        }
    }
}