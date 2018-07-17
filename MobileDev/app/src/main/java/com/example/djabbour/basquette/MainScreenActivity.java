package com.example.djabbour.basquette;


import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;


public class MainScreenActivity extends AppCompatActivity {

    public static MainScreenFragment newInstance() {
        MainScreenFragment fragment = new MainScreenFragment();
        return fragment;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_screen);

    }

}