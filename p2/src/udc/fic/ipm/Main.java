package udc.fic.ipm;

import android.app.Activity;
import android.app.Fragment;
import android.os.Bundle;
import android.content.Context;

import android.view.View;

import android.widget.Toast;


public class Main extends Activity 
{

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
			case 2: text = "Item Added";break;
			default: text = "Hello!";
		}

		Toast.makeText(context,text,duration).show();
	}

	public void addItem(String element){
		Item_List fragment = (Item_List) 
			getFragmentManager().findFragmentById(R.id.list_1);

		fragment.addItem(element);
	}
}
