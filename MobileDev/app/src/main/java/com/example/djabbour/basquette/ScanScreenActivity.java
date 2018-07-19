package com.example.djabbour.basquette;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;

public class ScanScreenActivity extends AppCompatActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scan_screen);

        BottomNavigationView bottomNavigationView = (BottomNavigationView)
                findViewById(R.id.navigation);

        Menu menu = bottomNavigationView.getMenu();
        MenuItem menuItem = menu.getItem(1);
        menuItem.setChecked(true);

        bottomNavigationView.setOnNavigationItemSelectedListener
                (new BottomNavigationView.OnNavigationItemSelectedListener() {

                    @Override
                    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                        switch (item.getItemId()){
                            case R.id.navigation_home:
                                Intent homeIntent = new Intent(ScanScreenActivity.this, MainScreenActivity.class);
                                startActivity(homeIntent);
                                break;

                            case R.id.navigation_scan:
                                break;

                            case R.id.navigation_settings:
                                Intent settingsIntent = new Intent(ScanScreenActivity.this, SettingScreenActivity.class);
                                startActivity(settingsIntent);
                                break;

                        }

                        return false;
                    }
                });
    }


}