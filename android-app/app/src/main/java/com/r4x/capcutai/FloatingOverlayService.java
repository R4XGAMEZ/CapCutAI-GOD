package com.r4x.capcutai;

import android.app.*;
import android.content.Intent;
import android.graphics.*;
import android.os.*;
import android.view.*;
import android.widget.*;
import androidx.core.app.NotificationCompat;

public class FloatingOverlayService extends Service {

    private WindowManager windowManager;
    private View floatingView;
    private WindowManager.LayoutParams params;
    private boolean isExpanded = false;

    private static final String CHANNEL_ID = "capcut_ai_overlay";

    @Override
    public void onCreate() {
        super.onCreate();
        createNotificationChannel();
        startForeground(1, buildNotification());
        createFloatingButton();
    }

    private void createFloatingButton() {
        windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);

        floatingView = LayoutInflater.from(this).inflate(R.layout.floating_overlay, null);

        params = new WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        );
        params.gravity = Gravity.TOP | Gravity.START;
        params.x = 0;
        params.y = 300;

        windowManager.addView(floatingView, params);
        setupTouchListener();
        setupButtons();
    }

    private void setupTouchListener() {
        View mainBtn = floatingView.findViewById(R.id.floating_main_btn);
        final int[] initialX = {0};
        final int[] initialY = {0};
        final float[] initialTouchX = {0};
        final float[] initialTouchY = {0};
        final boolean[] isDragging = {false};

        mainBtn.setOnTouchListener((v, event) -> {
            switch (event.getAction()) {
                case MotionEvent.ACTION_DOWN:
                    initialX[0] = params.x;
                    initialY[0] = params.y;
                    initialTouchX[0] = event.getRawX();
                    initialTouchY[0] = event.getRawY();
                    isDragging[0] = false;
                    return true;

                case MotionEvent.ACTION_MOVE:
                    float dx = event.getRawX() - initialTouchX[0];
                    float dy = event.getRawY() - initialTouchY[0];
                    if (Math.abs(dx) > 10 || Math.abs(dy) > 10) isDragging[0] = true;
                    if (isDragging[0]) {
                        params.x = initialX[0] + (int) dx;
                        params.y = initialY[0] + (int) dy;
                        windowManager.updateViewLayout(floatingView, params);
                    }
                    return true;

                case MotionEvent.ACTION_UP:
                    if (!isDragging[0]) toggleExpanded();
                    return true;
            }
            return false;
        });
    }

    private void setupButtons() {
        View panel = floatingView.findViewById(R.id.control_panel);

        // Screenshot + Send to AI
        floatingView.findViewById(R.id.btn_ai_analyze).setOnClickListener(v -> {
            Toast.makeText(this, "📸 Analyzing screen...", Toast.LENGTH_SHORT).show();
            new Thread(() -> {
                String path = "/sdcard/capcut_ai_screen.png";
                ShizukuBridge.takeScreenshot(path);
                // Notify socket server
                SocketServerService.broadcastCommand("SCREENSHOT_TAKEN:" + path);
            }).start();
        });

        // Open CapCut
        floatingView.findViewById(R.id.btn_open_capcut).setOnClickListener(v -> {
            ShizukuBridge.openCapCut();
        });

        // Emergency Stop
        floatingView.findViewById(R.id.btn_stop).setOnClickListener(v -> {
            SocketServerService.broadcastCommand("STOP");
            Toast.makeText(this, "🛑 Bot Stopped", Toast.LENGTH_SHORT).show();
        });

        // Quick tap at current screen
        floatingView.findViewById(R.id.btn_tap_center).setOnClickListener(v -> {
            int[] size = ShizukuBridge.getScreenSize();
            ShizukuBridge.tap(size[0]/2, size[1]/2);
        });
    }

    private void toggleExpanded() {
        View panel = floatingView.findViewById(R.id.control_panel);
        isExpanded = !isExpanded;
        panel.setVisibility(isExpanded ? View.VISIBLE : View.GONE);
    }

    private void createNotificationChannel() {
        NotificationChannel channel = new NotificationChannel(
            CHANNEL_ID, "CapCut AI Overlay",
            NotificationManager.IMPORTANCE_LOW);
        getSystemService(NotificationManager.class).createNotificationChannel(channel);
    }

    private Notification buildNotification() {
        return new NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("CapCut AI GOD Active")
            .setContentText("Overlay running | Tap to control")
            .setSmallIcon(android.R.drawable.ic_menu_camera)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build();
    }

    @Override
    public IBinder onBind(Intent intent) { return null; }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (floatingView != null) windowManager.removeView(floatingView);
    }
}
