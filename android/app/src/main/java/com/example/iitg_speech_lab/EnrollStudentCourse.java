package com.example.iitg_speech_lab;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.View;
import android.support.v7.widget.DefaultItemAnimator;
import android.support.v7.widget.LinearLayoutManager;
import android.widget.TextView;

import com.example.iitg_speech_lab.Class.EnrollMyData;
import com.example.iitg_speech_lab.Model.EnrollDataModel;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.android.gms.tasks.TaskCompletionSource;
import com.google.android.gms.tasks.Tasks;

import java.util.ArrayList;


public class EnrollStudentCourse extends AppCompatActivity {

    private static RecyclerView.Adapter adapter;
    private RecyclerView recyclerView;
    private static ArrayList<EnrollDataModel> data;
    static View.OnClickListener myOnClickListener;
    public TaskCompletionSource<Integer> task1;
    public Task task2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        String username = StudentCoursesActivity.username;
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_enroll_student_course);

        myOnClickListener = new MyOnClickListener();


        recyclerView = findViewById(R.id.student_enroll_course_recycler_view);
        recyclerView.setHasFixedSize(true);

        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(this);
        recyclerView.setLayoutManager(layoutManager);
        recyclerView.setItemAnimator(new DefaultItemAnimator());

        task1 = new TaskCompletionSource<>();
        task2 = task1.getTask();
        Log.d("yo",username);
        EnrollMyData.loadCourses(username,task1);

        Task<Void> allTask = Tasks.whenAll(task2);

        allTask.addOnSuccessListener(new OnSuccessListener<Void>() {
            @Override
            public void onSuccess(Void aVoid) {
                data = new ArrayList<>();
                Log.d("yo",Integer.toString(EnrollMyData.coursesIDList.size()));
                for (int i = 0; i < EnrollMyData.coursesIDList.size(); i++) {
                    data.add(new EnrollDataModel(
                            EnrollMyData.coursesIDList.get(i),
                            EnrollMyData.coursesNameList.get(i),
                            EnrollMyData.coursesProfList.get(i),
                            EnrollMyData.courseInfoList.get(i)
                    ));
                }

                adapter = new EnrollAdapter(data);
                recyclerView.setAdapter(adapter);
            }
        });
    }

    private class MyOnClickListener implements View.OnClickListener {

        private MyOnClickListener() {
        }

        @Override
        public void onClick(View v) {
            viewCourse(v);
        }

        private void viewCourse(View v) {
            int selectedItemPosition = recyclerView.getChildLayoutPosition(v);
            RecyclerView.ViewHolder viewHolder
                    = recyclerView.findViewHolderForLayoutPosition(selectedItemPosition);
            TextView textViewName
                    = null;
            if (viewHolder != null) {
                textViewName = viewHolder.itemView.findViewById(R.id.textViewCourseID);
            }
            String selectedName = null;
            if (textViewName != null) {
                selectedName = ( String ) textViewName.getText();
            }

            Log.d("aman",selectedName);
            String cinfo = null;
            if (viewHolder != null) {
                cinfo = (String) viewHolder.itemView.getTag();
            }
            Log.d("aman",cinfo);
            Intent intent = new Intent(EnrollStudentCourse.this, EnrollCourse.class);
            intent.putExtra("courseInfo",cinfo);
            startActivity(intent);
        }
    }



}
