package com.r4x.capcutai;

import android.app.*;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;
import androidx.core.app.NotificationCompat;
import org.json.JSONObject;
import java.io.*;
import java.net.*;
import java.util.concurrent.*;

public class SocketServerService extends Service {
    private static final String TAG = "SocketServer";
    private static final int PORT = 9999;
    private static final String CHANNEL_ID = "socket_server";

    private ServerSocket serverSocket;
    private ExecutorService executor = Executors.newCachedThreadPool();
    private static PrintWriter currentWriter;
    private boolean running = false;

    @Override
    public void onCreate() {
        super.onCreate();
        createNotificationChannel();
        startForeground(2, buildNotification());
        startServer();
    }

    private void startServer() {
        running = true;
        executor.execute(() -> {
            try {
                serverSocket = new ServerSocket(PORT);
                Log.d(TAG, "Server started on port " + PORT);
                while (running) {
                    Socket client = serverSocket.accept();
                    executor.execute(() -> handleClient(client));
                }
            } catch (Exception e) {
                Log.e(TAG, "Server error: " + e.getMessage());
            }
        });
    }

    private void handleClient(Socket client) {
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(client.getInputStream()));
            currentWriter = new PrintWriter(new OutputStreamWriter(client.getOutputStream()), true);

            Log.d(TAG, "Python bot connected!");
            currentWriter.println("{\"status\":\"connected\",\"device\":\"Vivo Y22 GOD MODE\"}");

            String line;
            while ((line = reader.readLine()) != null) {
                processCommand(line, currentWriter);
            }
        } catch (Exception e) {
            Log.e(TAG, "Client error: " + e.getMessage());
        }
    }

    private void processCommand(String json, PrintWriter writer) {
        try {
            JSONObject cmd = new JSONObject(json);
            String action = cmd.getString("action");
            JSONObject result = new JSONObject();

            switch (action) {
                case "tap":
                    ShizukuBridge.tap(cmd.getInt("x"), cmd.getInt("y"));
                    result.put("status", "ok");
                    break;

                case "swipe":
                    ShizukuBridge.swipe(
                        cmd.getInt("x1"), cmd.getInt("y1"),
                        cmd.getInt("x2"), cmd.getInt("y2"),
                        cmd.optInt("duration", 300)
                    );
                    result.put("status", "ok");
                    break;

                case "long_press":
                    ShizukuBridge.longPress(cmd.getInt("x"), cmd.getInt("y"));
                    result.put("status", "ok");
                    break;

                case "screenshot":
                    String path = "/sdcard/capcut_ai_screen.png";
                    ShizukuBridge.takeScreenshot(path);
                    result.put("status", "ok");
                    result.put("path", path);
                    break;

                case "shell":
                    String output = ShizukuBridge.exec(cmd.getString("command"));
                    result.put("status", "ok");
                    result.put("output", output);
                    break;

                case "type":
                    ShizukuBridge.typeText(cmd.getString("text"));
                    result.put("status", "ok");
                    break;

                case "key":
                    ShizukuBridge.keyEvent(cmd.getInt("keycode"));
                    result.put("status", "ok");
                    break;

                case "open_capcut":
                    ShizukuBridge.openCapCut();
                    result.put("status", "ok");
                    break;

                case "back":
                    ShizukuBridge.pressBack();
                    result.put("status", "ok");
                    break;

                case "get_screen_size":
                    int[] size = ShizukuBridge.getScreenSize();
                    result.put("width", size[0]);
                    result.put("height", size[1]);
                    result.put("status", "ok");
                    break;

                case "current_app":
                    result.put("output", ShizukuBridge.getCurrentApp());
                    result.put("status", "ok");
                    break;

                default:
                    result.put("status", "error");
                    result.put("message", "Unknown action: " + action);
            }

            writer.println(result.toString());

        } catch (Exception e) {
            try {
                JSONObject err = new JSONObject();
                err.put("status", "error");
                err.put("message", e.getMessage());
                writer.println(err.toString());
            } catch (Exception ignored) {}
        }
    }

    public static void broadcastCommand(String msg) {
        if (currentWriter != null) {
            currentWriter.println("{\"event\":\"" + msg + "\"}");
        }
    }

    private void createNotificationChannel() {
        NotificationChannel channel = new NotificationChannel(
            CHANNEL_ID, "Socket Server", NotificationManager.IMPORTANCE_LOW);
        getSystemService(NotificationManager.class).createNotificationChannel(channel);
    }

    private Notification buildNotification() {
        return new NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("CapCut AI - Bot Server")
            .setContentText("Python bot listening on port " + PORT)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .build();
    }

    @Override
    public IBinder onBind(Intent intent) { return null; }

    @Override
    public void onDestroy() {
        running = false;
        try { if (serverSocket != null) serverSocket.close(); } catch (Exception ignored) {}
        executor.shutdown();
    }
}
