package com.example.djabbour.basquette;


import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;

import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.components.Legend;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;

import java.util.ArrayList;

import static android.content.ContentValues.TAG;


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
        legend.setPosition(Legend.LegendPosition.LEFT_OF_CHART); //depracated, fix this

        //Create pie data object
        PieData pieData = new PieData(pieDataSet);
        pieChart.setData(pieData);
        pieChart.invalidate();

    }

}