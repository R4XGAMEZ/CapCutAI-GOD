package com.r4x.capcutai;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.GestureDescription;
import android.graphics.Path;
import android.util.Log;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import java.util.List;

public class CapCutAccessibilityService extends AccessibilityService {
    private static final String TAG = "CapCutA11y";
    private static CapCutAccessibilityService instance;

    @Override
    public void onServiceConnected() {
        instance = this;
        Log.d(TAG, "Accessibility Service Connected!");
    }

    public static CapCutAccessibilityService getInstance() {
        return instance;
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        // Log UI events for AI mapping
        if (event.getPackageName() != null &&
            event.getPackageName().toString().contains("lemon")) {
            Log.d(TAG, "CapCut Event: " + event.getEventType() +
                " | " + event.getContentDescription() +
                " | " + event.getText());
        }
    }

    @Override
    public void onInterrupt() {
        instance = null;
    }

    // === PERFORM TAP ===
    public static void performTap(float x, float y) {
        if (instance == null) return;
        GestureDescription.Builder builder = new GestureDescription.Builder();
        Path path = new Path();
        path.moveTo(x, y);
        builder.addStroke(new GestureDescription.StrokeDescription(path, 0, 50));
        instance.dispatchGesture(builder.build(), null, null);
    }

    // === FIND AND CLICK NODE BY TEXT ===
    public static boolean clickNodeWithText(String text) {
        if (instance == null) return false;
        AccessibilityNodeInfo root = instance.getRootInActiveWindow();
        if (root == null) return false;

        List<AccessibilityNodeInfo> nodes = root.findAccessibilityNodeInfosByText(text);
        for (AccessibilityNodeInfo node : nodes) {
            if (node.isClickable()) {
                node.performAction(AccessibilityNodeInfo.ACTION_CLICK);
                return true;
            }
            // Try parent
            AccessibilityNodeInfo parent = node.getParent();
            if (parent != null && parent.isClickable()) {
                parent.performAction(AccessibilityNodeInfo.ACTION_CLICK);
                return true;
            }
        }
        return false;
    }

    // === GET ALL VISIBLE TEXT ===
    public static String getAllVisibleText() {
        if (instance == null) return "";
        AccessibilityNodeInfo root = instance.getRootInActiveWindow();
        if (root == null) return "";
        StringBuilder sb = new StringBuilder();
        traverseNode(root, sb);
        return sb.toString();
    }

    private static void traverseNode(AccessibilityNodeInfo node, StringBuilder sb) {
        if (node == null) return;
        CharSequence text = node.getText();
        CharSequence desc = node.getContentDescription();
        if (text != null && text.length() > 0) sb.append(text).append("|");
        if (desc != null && desc.length() > 0) sb.append("[").append(desc).append("]|");
        for (int i = 0; i < node.getChildCount(); i++) {
            traverseNode(node.getChild(i), sb);
        }
    }

    // === SCROLL ===
    public static void performScroll(float x, float y, float endY) {
        if (instance == null) return;
        GestureDescription.Builder builder = new GestureDescription.Builder();
        Path path = new Path();
        path.moveTo(x, y);
        path.lineTo(x, endY);
        builder.addStroke(new GestureDescription.StrokeDescription(path, 0, 400));
        instance.dispatchGesture(builder.build(), null, null);
    }
}
