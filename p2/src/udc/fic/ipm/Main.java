package udc.fic.ipm;

import android.app.Activity;
import android.app.Fragment;
import android.os.Bundle;
import android.content.Context;

import android.view.View;

import android.widget.Toast;


public class Main extends Activity 
{

	//String element;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
    }

	public void throwToast(String txt){
		CharSequence text = (CharSequence) txt;
		Context context = getApplicationContext();
		int duration = Toast.LENGTH_SHORT;

		Toast.makeText(context,text,duration).show();
	}

	public void throwToast(int opt){

		CharSequence text;
		Context context = getApplicationContext();
		int duration = Toast.LENGTH_SHORT;

		switch(opt){
			case 1: text = "Item Already Exists!";break;
			case 2: text = "Item Deleted";break;
			case 3: text = "Erro Deleting";break;
			default: text = "Error";
		}

		Toast.makeText(context,text,duration).show();
	}

	public void addItem(String element){
		Item_List fragment = (Item_List) 
			getFragmentManager().findFragmentById(R.id.list_1);

		if(fragment == null) throwToast(3);
		else fragment.addItem(element);
	}

/*
	public void receiveItem(String item){
		element = item;
	}

	public String getNewItem(){
		Item_Add fragment = (Item_Add) 
			getFragmentManager().findFragmentById(R.id.add_1);

		if(fragment==null) return null;
		element = null;
		fragment.editItem();

		while (element == null){} 

		return element;

	}*/
}
