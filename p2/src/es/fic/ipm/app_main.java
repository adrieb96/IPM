package es.fic.ipm;

import android.app.Activity;
import android.os.Bundle;
import android.content.Context;

import android.widget.ListView;
import android.widget.ArrayAdapter;
import android.widget.Toast;
import android.widget.EditText;
import android.view.View;

import java.util.ArrayList;

public class app_main extends Activity{

	ArrayList<String> listItems = new ArrayList<String>();

	ArrayAdapter<String> adapter;

	int clickCounter = 0;

    @Override
    public void onCreate(Bundle icicle){
        super.onCreate(icicle);
        setContentView(R.layout.main);

		ListView listView = (ListView) findViewById(R.id.milista);

		adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, android.R.id.text1, listItems);
		listView.setAdapter(adapter);
    }

	public void throwToast(int opt){
		Context context = getApplicationContext();
		CharSequence text = "HELLO!!";
		int duration = Toast.LENGTH_SHORT;
		if (opt==1){
			text = "Item Already Exists!";
		}	
		
		Toast.makeText(context,text,duration).show();
	}

	public void sendMessage(View v){

		EditText editText = (EditText) findViewById(R.id.text_edit);
		String element = editText.getText().toString().trim();

		editText.setText("");
		if(element.length()<1) return;
		if(!addElement(element)) throwToast(1);
		else adapter.notifyDataSetChanged();
		/*
		listItems.add("Clicked: "+clickCounter++);
		adapter.notifyDataSetChanged();*/
	}

	public boolean addElement(String element){
		int i = 0;
		for(String e:listItems){
			if(e.compareToIgnoreCase(element)==0){
				return false;	
			}else if(e.compareToIgnoreCase(element)>0){
				break;
			}
			i++;
		}
		listItems.add(i,element);
		return true;
	}

	
}
