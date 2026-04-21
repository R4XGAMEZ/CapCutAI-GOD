package com.r4x.capcutai;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;
import rikka.shizuku.Shizuku;

public class MainActivity extends AppCompatActivity {

    private static final int SHIZUKU_REQUEST_CODE = 100;
    private TextView statusText;
    private Button btnStartOverlay, btnSettings, btnStartBot, btnStopBot;
    private Switch switchAccessibility;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        statusText = findViewById(R.id.status_text);
        btnStartOverlay = findViewById(R.id.btn_start_overlay);
        btnSettings = findViewById(R.id.btn_settings);
        btnStartBot = findViewById(R.id.btn_start_bot);
        btnStopBot = findViewById(R.id.btn_stop_bot);
        switchAccessibility = findViewById(R.id.switch_accessibility);

        checkPermissions();
        setupButtons();
        initShizuku();
    }

    private void checkPermissions() {
        // Check overlay permission
        if (!Settings.canDrawOverlays(this)) {
            Intent intent = new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                    Uri.parse("package:" + getPackageName()));
            startActivityForResult(intent, 1001);
        }
    }

    private void initShizuku() {
        Shizuku.addRequestPermissionResultListener((requestCode, grantResult) -> {
            if (grantResult == android.content.pm.PackageManager.PERMISSION_GRANTED) {
                updateStatus("✅ Shizuku Connected - GOD MODE READY");
            } else {
                updateStatus("❌ Shizuku Permission Denied");
            }
        });

        if (Shizuku.checkSelfPermission() == android.content.pm.PackageManager.PERMISSION_GRANTED) {
            updateStatus("✅ Shizuku Active - GOD MODE");
        } else if (Shizuku.shouldShowRequestPermissionRationale()) {
            updateStatus("⚠️ Shizuku needs permission");
        } else {
            Shizuku.requestPermission(SHIZUKU_REQUEST_CODE);
        }
    }

    private void setupButtons() {
        btnStartOverlay.setOnClickListener(v -> {
            Intent intent = new Intent(this, FloatingOverlayService.class);
            startForegroundService(intent);
            updateStatus("🟢 Floating Overlay Started");
        });

        btnSettings.setOnClickListener(v -> {
            startActivity(new Intent(this, SettingsActivity.class));
        });

        btnStartBot.setOnClickListener(v -> {
            // Start Socket Server + notify Python bot
            Intent intent = new Intent(this, SocketServerService.class);
            startForegroundService(intent);
            updateStatus("🤖 AI Bot Server Started on port 9999");
            Toast.makeText(this, "Run python bot in Termux!", Toast.LENGTH_LONG).show();
        });

        btnStopBot.setOnClickListener(v -> {
            stopService(new Intent(this, SocketServerService.class));
            updateStatus("🔴 Bot Server Stopped");
        });

        switchAccessibility.setOnCheckedChangeListener((btn, checked) -> {
            if (checked) {
                // Open accessibility settings
                startActivity(new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS));
            }
        });
    }

    private void updateStatus(String msg) {
        runOnUiThread(() -> statusText.setText(msg));
    }
}
