package com.r4x.capcutai;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;

public class SettingsActivity extends AppCompatActivity {

    private SharedPreferences prefs;
    private EditText etApiKey, etBotPort;
    private Spinner spinnerModel, spinnerSpeed, spinnerTarget;
    private Button btnSave;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        prefs = getSharedPreferences("capcut_ai", MODE_PRIVATE);

        etApiKey = findViewById(R.id.et_api_key);
        etBotPort = findViewById(R.id.et_bot_port);
        spinnerModel = findViewById(R.id.spinner_model);
        spinnerSpeed = findViewById(R.id.spinner_speed);
        spinnerTarget = findViewById(R.id.spinner_target);
        btnSave = findViewById(R.id.btn_save);

        // Model options
        ArrayAdapter<String> modelAdapter = new ArrayAdapter<>(this,
            android.R.layout.simple_spinner_item,
            new String[]{
                "anthropic/claude-opus-4",
                "anthropic/claude-sonnet-4-5",
                "openai/gpt-4o",
                "google/gemini-2.0-flash",
                "meta-llama/llama-3.2-90b-vision-instruct",
                "google/gemini-pro-vision"
            });
        spinnerModel.setAdapter(modelAdapter);

        // Speed options
        ArrayAdapter<String> speedAdapter = new ArrayAdapter<>(this,
            android.R.layout.simple_spinner_item,
            new String[]{"FAST (0.5s delay)", "NORMAL (1s delay)", "SLOW (2s delay)"});
        spinnerSpeed.setAdapter(speedAdapter);

        // Target app
        ArrayAdapter<String> targetAdapter = new ArrayAdapter<>(this,
            android.R.layout.simple_spinner_item,
            new String[]{"CapCut", "VN Video Editor", "InShot", "Kinemaster"});
        spinnerTarget.setAdapter(targetAdapter);

        loadSettings();

        btnSave.setOnClickListener(v -> saveSettings());
    }

    private void loadSettings() {
        etApiKey.setText(prefs.getString("api_key", ""));
        etBotPort.setText(String.valueOf(prefs.getInt("bot_port", 9999)));
        spinnerModel.setSelection(prefs.getInt("model_index", 0));
        spinnerSpeed.setSelection(prefs.getInt("speed_index", 1));
        spinnerTarget.setSelection(prefs.getInt("target_index", 0));
    }

    private void saveSettings() {
        prefs.edit()
            .putString("api_key", etApiKey.getText().toString().trim())
            .putInt("bot_port", Integer.parseInt(etBotPort.getText().toString()))
            .putInt("model_index", spinnerModel.getSelectedItemPosition())
            .putInt("speed_index", spinnerSpeed.getSelectedItemPosition())
            .putInt("target_index", spinnerTarget.getSelectedItemPosition())
            .putString("model_name", spinnerModel.getSelectedItem().toString())
            .apply();

        Toast.makeText(this, "✅ Settings Saved!", Toast.LENGTH_SHORT).show();
        finish();
    }
}
