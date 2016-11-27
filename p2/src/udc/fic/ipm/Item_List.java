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
import android.view.View.OnClickListener;

import android.widget.AdapterView;
import android.widget.AdapterView.AdapterContextMenuInfo;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Item_List extends Fragment{

	ArrayList<String> categories_list = new ArrayList<String>();

	ArrayAdapter<String> adapter;

	ListView listView;
	Button button;

	String selected;

	private State state;

	private enum State{
		ADD,
		EDIT};


	public Item_List(){
		state = State.ADD;
	}

    /** Called when the activity is first created. */
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, 
			Bundle savedInstanceState){

		View rootView = inflater.inflate(R.layout.item_list,container,false);
		listView = (ListView) rootView.findViewById(R.id.list);
		button = (Button) rootView.findViewById(R.id.add_button);

		//categories_list.add("Vigo");
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

		//Button listener
		button.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v){
				String text = getEditText();
				if(state.equals(State.ADD)){
					addItem(text);
				}else{
					if(text.length()<1) return;
					editItem(text);
				}
				state = State.ADD;
				button.setText("Add");
				refreshView();
			}
		});

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

		selected = 
			listView.getAdapter().getItem(info.position).toString();

		switch(item.getItemId()){
			case R.id.menu_edit: 
				state = State.EDIT;
				button.setText("Edit");
				return true;
			case R.id.menu_delete:
				if(deleteItem(selected)) throwToast(2);
				else throwToast(3);
				refreshView();
				return true;
			default:
				return super.onContextItemSelected(item);
		}
	}

	public String getEditText(){
		EditText editText = (EditText) getView().findViewById(R.id.text_edit);
		String element = editText.getText().toString().trim();

		editText.setText("");
		return element;
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

		if(item.compareToIgnoreCase(selected)==0) return;;

		int i = 0;

		for(String e: categories_list){
			if(e.compareToIgnoreCase(item)==0){
				throwToast(1);
				return;
			}if(e.compareToIgnoreCase(item)>0){
				break;
			}
			i++;
		}

		if(deleteItem(selected)){
			addItem(item);
		}
		else throwToast(0);
	}

	public boolean deleteItem(String item){
		return categories_list.remove(item);	
	}

	public void addItem(String text){
		if(text.length()<1) return;

		int i = 0;
		for(String e: categories_list){
			if(e.compareToIgnoreCase(text)==0){
				throwToast(1);
				return;
			}if(e.compareToIgnoreCase(text)>0){
				break;
			}
			i++;
		}

		//if(categories_list.contains(text)) throwToast(1);

		categories_list.add(i,text);
	}
}
