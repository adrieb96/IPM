package udc.fic.ipm;

import android.app.Activity;
import android.app.Fragment;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.os.Bundle;
import android.content.Context;

import android.hardware.SensorManager;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.Sensor;

import android.view.View;

import android.widget.Toast;
import android.widget.TextView;

import java.util.ArrayList;
import android.util.Log;

import udc.fic.ipm.ShakeDetector.OnShakeListener;

public class Main extends Activity
{

	private SensorManager mSensorManager;
	private Sensor mAccelerometer;
	private Sensor mMagnetic;
	private ShakeDetector mShakeDetector;
	private int level = 0;

	ArrayList<Category> categories_list;	
	String titleOfCategory = null;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

		//Initialize ShakeDetector
		mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
		mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
		mMagnetic = mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
		mShakeDetector = new ShakeDetector();
		mShakeDetector.setOnShakeListener(new OnShakeListener(){
			@Override
			public void onShake(){
				handleShakeEvent("shake");
			}

			@Override
			public void onFaceDown(){
				handleShakeEvent("Face Down");
			}

			@Override
			public void onRotation(){
				handleShakeEvent("Rotation");
			}

			@Override  
			public void onMovement(){
				Log.i("MOVEMENT", "MOVEMENT DETECTED");
			}

			@Override
			public void onMovement(String str){
				Log.i("MOVEMENT", str);
			}
		});

		if(findViewById(R.id.main_container) != null){

			//if we are being restored return
			if(savedInstanceState != null) return;

			categories_list = new ArrayList<Category>();

			Category_List fragment_1 = new Category_List();

			getFragmentManager().beginTransaction().add(
					R.id.main_container, fragment_1).commit();

		}
    }
	
	@Override
	public void onResume(){
		super.onResume();
		mSensorManager.registerListener(mShakeDetector, mAccelerometer, 
				SensorManager.SENSOR_DELAY_UI);
		mSensorManager.registerListener(mShakeDetector, mMagnetic, 
				SensorManager.SENSOR_DELAY_UI);
	}
	
	@Override
	public void onPause(){
		mSensorManager.unregisterListener(mShakeDetector);
		super.onPause();
	}

	@Override
	public void onBackPressed(){
		level--;
		if(level < 1) titleOfCategory = null;
		Log.i("MY_ACTIVITY","ACTUAL LEVEL = " + level);
		Log.i("MY_ACTIVITY","ACTUAL ITEM  = " + ((titleOfCategory == null)? "null" : titleOfCategory));

		super.onBackPressed();
	}


	public void handleShakeEvent(String mode){
		Log.i("MY_ACTIVITY",mode);
		if(titleOfCategory!=null){
			Category cat = searchCategory(titleOfCategory);
			ArrayList<String> items = cat.getItems();

			String item = null;
			int size = items.size();
			if(size>0){
				int random = (int)(Math.random() * size);
				item = items.get(random);
			}

			Show_Item fragment = new Show_Item(item);

			FragmentManager mngr = getFragmentManager();
			FragmentTransaction transaction = mngr.beginTransaction();

			transaction.replace(R.id.main_container, fragment);
			
			transaction.addToBackStack(null);
			level++;
			//only adds the fragment to stack if is showing category
			if(level>2){
				mngr.popBackStack();
				level--;
				Log.i("MY_ACTIVITY", "ALREADY SHOWING AN ITEM");
			}
			transaction.commit();

		}else{
			Log.i("MY_ACTIVITY","Not Item Selected");
		}
	}

	public void showCategory(String category){
		Category cat = searchCategory(category);

		if(cat == null) return;

		ArrayList<String> items = cat.getItems();
		String title = cat.getTitle();
		titleOfCategory = title;

		Item_List fragment = new Item_List(title, items);

		FragmentTransaction transaction = 
			getFragmentManager().beginTransaction();

		transaction.replace(R.id.main_container, fragment);
		transaction.addToBackStack(null);

		level++;

		transaction.commit();
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

	public boolean addItem(String title){
		return categories_list.add(new Category(title));
	}

	public boolean deleteItem(String title){
		return categories_list.remove(searchCategory(title));
	}

	public boolean changeItem(String old, String title){
		Category cat = searchCategory(old);

		if(cat == null) return false;

		cat.setTitle(title);
		return true;
	}

	public void passItems(String title, ArrayList<String> items){
		searchCategory(title).setItems(items);
	}

	public Category searchCategory(String title){
		for(Category cat: categories_list){
			if(cat.getTitle().equals(title)) return cat;
		}
		return null;
	}
}
