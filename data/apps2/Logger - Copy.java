import java.io.FileWriter;

public class Logger {
    public static void main(String[] args) {
        try (FileWriter fw = new FileWriter("log.txt", true)) {
            fw.write("Event: " + args[0] + " at " + System.currentTimeMillis() + "\n");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}