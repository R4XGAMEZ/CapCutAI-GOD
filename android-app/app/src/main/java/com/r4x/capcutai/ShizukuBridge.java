package com.r4x.capcutai;

import android.content.pm.PackageManager;
import android.util.Log;
import rikka.shizuku.Shizuku;
import rikka.shizuku.ShizukuRemoteProcess;

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
            ShizukuRemoteProcess process = Shizuku.newProcess(
                new String[]{"sh", "-c", command}, null, null);
            byte[] output = process.getInputStream().readAllBytes();
            process.waitFor();
            return new String(output).trim();
        } catch (Exception e) {
            Log.e(TAG, "exec failed: " + e.getMessage());
            return "ERROR: " + e.getMessage();
        }
    }

    // === TAP ===
    public static void tap(int x, int y) {
        exec("input tap " + x + " " + y);
        Log.d(TAG, "TAP: " + x + "," + y);
    }

    // === SWIPE ===
    public static void swipe(int x1, int y1, int x2, int y2, int duration) {
        exec("input swipe " + x1 + " " + y1 + " " + x2 + " " + y2 + " " + duration);
    }

    // === LONG PRESS ===
    public static void longPress(int x, int y) {
        exec("input swipe " + x + " " + y + " " + x + " " + y + " 1000");
    }

    // === KEY EVENT ===
    public static void keyEvent(int keyCode) {
        exec("input keyevent " + keyCode);
    }

    // === BACK ===
    public static void pressBack() {
        keyEvent(4);
    }

    // === HOME ===
    public static void pressHome() {
        keyEvent(3);
    }

    // === SCREENSHOT ===
    public static String takeScreenshot(String path) {
        return exec("screencap -p " + path);
    }

    // === LAUNCH APP ===
    public static void launchApp(String packageName) {
        exec("monkey -p " + packageName + " -c android.intent.category.LAUNCHER 1");
    }

    // === OPEN CAPCUT ===
    public static void openCapCut() {
        launchApp("com.lemon.lvoverseas"); // CapCut package
    }

    // === TYPE TEXT ===
    public static void typeText(String text) {
        // Escape spaces
        String escaped = text.replace(" ", "%s");
        exec("input text " + escaped);
    }

    // === SCROLL ===
    public static void scrollDown(int centerX, int centerY) {
        swipe(centerX, centerY + 300, centerX, centerY - 300, 300);
    }

    public static void scrollUp(int centerX, int centerY) {
        swipe(centerX, centerY - 300, centerX, centerY + 300, 300);
    }

    // === GET SCREEN SIZE ===
    public static int[] getScreenSize() {
        String result = exec("wm size");
        // "Physical size: 720x1600"
        try {
            String[] parts = result.split(": ")[1].split("x");
            return new int[]{Integer.parseInt(parts[0].trim()), Integer.parseInt(parts[1].trim())};
        } catch (Exception e) {
            return new int[]{720, 1600}; // Vivo Y22 default
        }
    }

    // === CURRENT APP ===
    public static String getCurrentApp() {
        return exec("dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'");
    }
}
