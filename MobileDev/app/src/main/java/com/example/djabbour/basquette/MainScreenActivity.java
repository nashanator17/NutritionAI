package com.example.djabbour.basquette;


import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;

import com.github.mikephil.charting.charts.PieChart;


public class MainScreenActivity extends AppCompatActivity {

    private static String TAG = "MainActivity";

    private float[] yData = {25.3f, 10.6f, 66.76f};
    private String[] xData = {"Carbs", "Fats", "Proteins"};
    PieChart pieChart;

    public static MainScreenFragment newInstance() {
        MainScreenFragment fragment = new MainScreenFragment();
        return fragment;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_screen);

        //Logs details about activity it is working in
        Log.d(TAG, "onCreate: Starting to create chart");
        
    }

}