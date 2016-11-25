package udc.fic.ipm;

import android.app.Fragment;
import android.os.Bundle;

import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.view.View;

import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.List;

public class Item_List extends Fragment{

	ArrayList<String> categories_list = new ArrayList<String>();

	ArrayAdapter<String> adapter;

	ListView listView;

    /** Called when the activity is first created. */
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, 
			Bundle savedInstanceState){

		listView = (ListView) getView().findViewById(R.id.list);

		categories_list.add("Vigo");
		categories_list.add("Alemania");
		categories_list.add("Portugal");

		adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, android.R.id.text1, categories_list);

		listView.setAdapter(adapter);

		return listView;
    }

}
