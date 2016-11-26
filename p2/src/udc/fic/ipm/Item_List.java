package udc.fic.ipm;

import android.app.Fragment;
import android.os.Bundle;

import android.view.ContextMenu;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.MenuInflater;
import android.view.ViewGroup;
import android.view.View;

import android.widget.AdapterView;
import android.widget.AdapterView.AdapterContextMenuInfo;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Item_List extends Fragment{

	ArrayList<String> categories_list = new ArrayList<String>();

	ArrayAdapter<String> adapter;

	ListView listView;

	public Item_List(){}

    /** Called when the activity is first created. */
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, 
			Bundle savedInstanceState){

		View rootView = inflater.inflate(R.layout.item_list,container,false);
		listView = (ListView) rootView.findViewById(R.id.list);

		adapter = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_list_item_1, android.R.id.text1, categories_list);

		listView.setAdapter(adapter);

		registerForContextMenu(listView);
		/*listView.setOnClickListener(new OnItemClickListener(){
			@Override
			public void onItemClick(AdapterView<?> arg0, View arg1,
					int position, long arg3){
				String category = categories_list.get(position);
				//Class ac
			}
		});*/

		return rootView;
    }

	@Override
	public void onCreateContextMenu(ContextMenu menu, View v, ContextMenuInfo menuInfo){
		super.onCreateContextMenu(menu, v, menuInfo);
		MenuInflater inflater = ((Main)getActivity()).getMenuInflater();

		AdapterContextMenuInfo info = (AdapterContextMenuInfo) menuInfo;

		String selected = listView.getAdapter().getItem(info.position).toString();

		menu.setHeaderTitle(selected);
		inflater.inflate(R.menu.menu, menu);
	}

	@Override
	public boolean onContextItemSelected(MenuItem item){
		AdapterContextMenuInfo info = 
			(AdapterContextMenuInfo) item.getMenuInfo();

		String element = 
			listView.getAdapter().getItem(info.position).toString();

		switch(item.getItemId()){
			case R.id.menu_edit: 
				editItem(element); 
				break;
			case R.id.menu_delete:
				if(deleteItem(element)) throwToast(2);
				else throwToast(3);
				break;
			default:
				return super.onContextItemSelected(item);
		}
		refreshView();
		return true;
	}

	public void refreshView(){
		listView.setAdapter(new ArrayAdapter<String>(getActivity(), android.R.layout.simple_list_item_1, android.R.id.text1, categories_list));
	}

	private void throwToast(int n){
		((Main)getActivity()).throwToast(n);
	}

	private void ordenar(){
		Collections.sort(categories_list);
	}

	public void editItem(String item){
		//String new_item = ((Main)getActivity()).getNewItem();
		String new_item = "aaaa";
		if(item == new_item) return;

		if(categories_list.contains(new_item)) throwToast(1);
		else{
			if(deleteItem(item)){
				addItem(new_item);
			}
			else throwToast(0);
		}
	}

	public boolean deleteItem(String item){
		return categories_list.remove(item);	
	}

	public void addItem(String text){
		if(categories_list.contains(text)) throwToast(1);

		categories_list.add(text);
		refreshView();

	}
}
