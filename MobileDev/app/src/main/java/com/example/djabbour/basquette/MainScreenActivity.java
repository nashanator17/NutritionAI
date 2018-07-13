package com.example.djabbour.basquette;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;
import android.widget.TextView;

public class MainScreenActivity extends AppCompatActivity {

    private TextView mTextMessage;

    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        //Use switch cases to navigate to another screen
        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            switch (item.getItemId()) {
                case R.id.navigation_home:
                    break;

                case R.id.navigation_scan:
                    Intent intent1 = new Intent(MainScreenActivity.this, ScanScreenActivity.class);
                    startActivity(intent1);
                    break;

                case R.id.navigation_settings:
                    Intent intent2 = new Intent(MainScreenActivity.this, ScanScreenActivity.class);
                    startActivity(intent2);
                    break;

            }

            return false;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_screen);
        System.loadLibrary("opencv_java3");

        mTextMessage = (TextView) findViewById(R.id.message);
        BottomNavigationView navigation = (BottomNavigationView) findViewById(R.id.navigation);
        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);

    }
}

