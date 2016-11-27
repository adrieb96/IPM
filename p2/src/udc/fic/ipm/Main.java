package udc.fic.ipm;

import android.app.Activity;
import android.app.Fragment;
import android.app.FragmentTransaction;
import android.os.Bundle;
import android.content.Context;

import android.view.View;

import android.widget.Toast;
import java.util.ArrayList;

public class Main extends Activity 
{

	ArrayList<Category> categories_list;	

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

		if(findViewById(R.id.main_container) != null){

			//if we are being restored return
			if(savedInstanceState != null) return;

			categories_list = new ArrayList<Category>();

			Category_List fragment_1 = new Category_List();

			getFragmentManager().beginTransaction().add(
					R.id.main_container, fragment_1).commit();

		}
    }

	public void showCategory(String category){
		Category cat = searchCategory(category);

		if(cat == null) return;

		ArrayList<String> items = cat.getItems();
		String title = cat.getTitle();

		Item_List fragment = new Item_List(title, items);

		FragmentTransaction transaction = 
			getFragmentManager().beginTransaction();

		transaction.replace(R.id.main_container, fragment);
		transaction.addToBackStack(null);

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
