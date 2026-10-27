import java.io.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Logger {
    public static void main(String[] args) {
        // If no arguments are passed, just exit
        if (args.length == 0)
            return;

        // Combine arguments into a single message
        String message = String.join(" ", args);

        try (FileWriter fw = new FileWriter("game_log.txt", true);
                PrintWriter out = new PrintWriter(fw)) {

            DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
            LocalDateTime now = LocalDateTime.now();

            // Write timestamp and message to the file
            out.println("[" + dtf.format(now) + "] " + message);

            // Also print to console so we see it in the Batch window
            System.out.println("[JAVA LOGGER] Saved event: " + message);

        } catch (IOException e) {
            System.err.println("Logger Error: " + e.getMessage());
        }
    }
}