package es.fic.ipm;

import android.app.Activity;
import android.os.Bundle;
import android.content.Context;

import android.widget.ListView;
import android.widget.AdapterView;
import android.widget.AdapterView.AdapterContextMenuInfo;
import android.widget.ArrayAdapter;
import android.widget.Toast;
import android.widget.EditText;

import android.view.ContextMenu;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.inputmethod.InputMethodManager;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;

import java.util.ArrayList;

public class app_main extends Activity{

	ArrayList<String> listItems = new ArrayList<String>();

	ArrayAdapter<String> adapter;

	ListView listView;

	boolean editing = false;
	String old = "";
	
    @Override
    public void onCreate(Bundle icicle){
        super.onCreate(icicle);
        setContentView(R.layout.main);

		listView = (ListView) findViewById(R.id.milista);

		registerForContextMenu(listView);

		adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, android.R.id.text1, listItems);
		listView.setAdapter(adapter);
    }

	@Override
	public void onCreateContextMenu(ContextMenu menu, View v, ContextMenuInfo menuInfo){
		super.onCreateContextMenu(menu,v,menuInfo);

		MenuInflater inflater = getMenuInflater();

		AdapterContextMenuInfo info = 
			(AdapterContextMenuInfo) menuInfo;
		
		menu.setHeaderTitle(listView.getAdapter().getItem(info.position).toString());

		inflater.inflate(R.menu.menu, menu);
	}

	@Override
	public boolean onContextItemSelected(MenuItem item){
		AdapterContextMenuInfo info = 
			(AdapterContextMenuInfo) item.getMenuInfo();

		String element = listView.getAdapter().getItem(info.position).toString();
		switch(item.getItemId()){
			case R.id.MenuEdit:	editElement(element);
								return true;
			case R.id.MenuDelete: throwToast(3); 
								  deleteElement(element);
								  return true;
			default: 
				return super.onContextItemSelected(item);
		}
	}


	public void throwToast(int opt){
		Context context = getApplicationContext();
		CharSequence text = "HELLO!!";
		int duration = Toast.LENGTH_SHORT;
		switch(opt){
			case 1: text = "Item Already Exists!"; break;
			case 2: text = (CharSequence) getResources().getString(R.string.edited); 
					break;
			case 3: text = "Delete Selected!"; break;
			default: break;
		}
		
		Toast.makeText(context,text,duration).show();
	}

	public void sendMessage(View v){

		EditText editText = (EditText) findViewById(R.id.text_edit);
		String element = editText.getText().toString().trim();

		InputMethodManager inputManager = (InputMethodManager) 
			getSystemService(Context.INPUT_METHOD_SERVICE);

		inputManager.hideSoftInputFromWindow(editText.
				getWindowToken(), 0);

		editText.setText("");
		if(element.length()<1) return;
		if(!addElement(element)) throwToast(1);
		else{
			if(editing){
				deleteElement(old);
				old="";
				editing=false;
				throwToast(2);
			}
			adapter.notifyDataSetChanged();
		}
		/*
		listItems.add("Clicked: "+clickCounter++);
		adapter.notifyDataSetChanged();*/
	}


	public void editElement(String element){

		EditText editText = (EditText) findViewById(R.id.text_edit);

		InputMethodManager inputManager = (InputMethodManager) 
			getSystemService(Context.INPUT_METHOD_SERVICE);

		inputManager.showSoftInput(editText, InputMethodManager.SHOW_IMPLICIT);
		old = element;
		editing = true;
	}

	public void deleteElement(String element){
		if(listItems.remove(element))
			adapter.notifyDataSetChanged();

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
