package com.r4x.capcutai;

import android.content.pm.PackageManager;
import android.util.Log;
import java.io.*;
import rikka.shizuku.Shizuku;

public class ShizukuBridge {
    private static final String TAG = "ShizukuBridge";

    public static boolean isAvailable() {
        try {
            return Shizuku.pingBinder() &&
                   Shizuku.checkSelfPermission() == PackageManager.PERMISSION_GRANTED;
        } catch (Exception e) {
            return false;
        }
    }

    public static String exec(String command) {
        if (!isAvailable()) return "ERROR: Shizuku not available";
        try {
            Process process = Runtime.getRuntime().exec(new String[]{"sh", "-c", command});
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) sb.append(line).append("\n");
            process.waitFor();
            return sb.toString().trim();
        } catch (Exception e) {
            Log.e(TAG, "exec failed: " + e.getMessage());
            return "ERROR: " + e.getMessage();
        }
    }

    public static void tap(int x, int y) {
        exec("input tap " + x + " " + y);
    }

    public static void swipe(int x1, int y1, int x2, int y2, int duration) {
        exec("input swipe " + x1 + " " + y1 + " " + x2 + " " + y2 + " " + duration);
    }

    public static void longPress(int x, int y) {
        exec("input swipe " + x + " " + y + " " + x + " " + y + " 1000");
    }

    public static void keyEvent(int keyCode) {
        exec("input keyevent " + keyCode);
    }

    public static void pressBack() { keyEvent(4); }
    public static void pressHome() { keyEvent(3); }

    public static String takeScreenshot(String path) {
        return exec("screencap -p " + path);
    }

    public static void launchApp(String packageName) {
        exec("monkey -p " + packageName + " -c android.intent.category.LAUNCHER 1");
    }

    public static void openCapCut() {
        launchApp("com.lemon.lvoverseas");
    }

    public static void typeText(String text) {
        String escaped = text.replace(" ", "%s");
        exec("input text " + escaped);
    }

    public static void scrollDown(int centerX, int centerY) {
        swipe(centerX, centerY + 300, centerX, centerY - 300, 300);
    }

    public static void scrollUp(int centerX, int centerY) {
        swipe(centerX, centerY - 300, centerX, centerY + 300, 300);
    }

    public static int[] getScreenSize() {
        String result = exec("wm size");
        try {
            String[] parts = result.split(": ")[1].split("x");
            return new int[]{Integer.parseInt(parts[0].trim()), Integer.parseInt(parts[1].trim())};
        } catch (Exception e) {
            return new int[]{720, 1600};
        }
    }

    public static String getCurrentApp() {
        return exec("dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'");
    }
}
