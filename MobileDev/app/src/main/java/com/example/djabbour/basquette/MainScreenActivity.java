package com.example.djabbour.basquette;


import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;

import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.components.Legend;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;

import java.util.ArrayList;

public class MainScreenActivity extends AppCompatActivity {

    private static String TAG = "MainActivity";

    private float[] yData = {25.3f, 10.6f, 66.76f};
    private String[] xData = {"Carbs", "Fats", "Proteins"};
    PieChart pieChart;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_screen);

        BottomNavigationView bottomNavigationView = (BottomNavigationView)
                findViewById(R.id.navigation);

        Menu menu = bottomNavigationView.getMenu();
        MenuItem menuItem = menu.getItem(0);
        menuItem.setChecked(true);

        bottomNavigationView.setOnNavigationItemSelectedListener
                (new BottomNavigationView.OnNavigationItemSelectedListener() {

                    @Override
                    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                        switch (item.getItemId()){
                            case R.id.navigation_home:
                                break;

                            case R.id.navigation_scan:
                                Intent scanIntent = new Intent(MainScreenActivity.this, ScanScreenActivity.class);
                                scanIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                                startActivity(scanIntent);
                                break;

                            case R.id.navigation_settings:
                                Intent settingsIntent = new Intent(MainScreenActivity.this, SettingScreenActivity.class);
                                settingsIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                                startActivity(settingsIntent);
                                break;

                        }

                        return false;
                    }
                });

        //Logs details about activity it is working in
        Log.d(TAG, "onCreate: Starting to create chart");
        pieChart = (PieChart) findViewById(R.id.pieChart);


//        pieChart.setDescription("Nutrient percentages");
        pieChart.setRotationEnabled(true);
        pieChart.setHoleRadius(30f);
        addDataSet();

    }

    private void addDataSet() {
        Log.d(TAG, "addDataSet has begun");
        ArrayList<PieEntry> yEntries = new ArrayList<>();
        ArrayList<String> xEntries = new ArrayList<>();

        for(int i=0;i<yData.length;i++){
            yEntries.add(new PieEntry(yData[i], i));
        }

        for(int i=1;i<xData.length;i++){
            xEntries.add(xData[i]);
        }

        //Create data set
        PieDataSet pieDataSet = new PieDataSet(yEntries, "Nutrients");
        pieDataSet.setSliceSpace(1);
        pieDataSet.setValueTextSize(8);

        ArrayList<Integer> colors = new ArrayList<>();
        colors.add(Color.BLUE);
        colors.add(Color.RED);
        colors.add(Color.GREEN);

        pieDataSet.setColors(colors);

        //Add legend to chart

        Legend legend = pieChart.getLegend();
        legend.setForm(Legend.LegendForm.CIRCLE);

        //Create pie data object
        PieData pieData = new PieData(pieDataSet);
        pieChart.setData(pieData);
        pieChart.invalidate();

    }

}