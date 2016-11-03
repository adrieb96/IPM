package es.fic.ipm;

import android.app.Activity;
import android.os.Bundle;

import android.widget.TextView;
import android.widget.ListView;
import android.widget.EditText;
import android.widget.ArrayAdapter;
import android.widget.Toast;

import android.view.ContextMenu;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.MenuItem;
import android.view.View;

import java.util.ArrayList;
import java.util.List;

public class ipm_main extends Activity{
	
	public List<String> lista = new ArrayList<String>();

	ArrayAdapter<String> adapter;
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle icicle){
        super.onCreate(icicle);
        setContentView(R.layout.main2);
		
		TextView message = (TextView) findViewById(R.id.message);
		ListView listView = (ListView) findViewById(R.id.milista);

		adapter = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,android.R.id.text1, lista);
		listView.setAdapter(adapter);

		registerForContextMenu(listView);
		/*TextView tv = new TextView(this);
		tv.setText("Hello World");
		setContentView(tv);
		*/
    }

	/** Creates a Context Menu */
/*	@Override
	public void onCreateContextMenu(ContextMenu menu, View v, ContextMenuInfo menuInfo){
		super.onCreateContextMenu(menu, v, menuInfo);
		MenuInflater inflater = getMenuInflater();

		AdapterView.AdapterContextMenuInfo info = 
			(AdapterView.AdapterContextMenuInfo) menuInfo;

		menu.setHeaderTitle(
			listView.getAdapter().getItem(info.position).toString());
		inflater.inflate(R.menu.ctx_menu,menu);
	}

	@Override
	public boolean onContextItemSelected(MenuItem item){

		AdapterContextMenuInfo info = (AdapterContextMenuInfo) item.getMenuInfo();
		switch(item.getItemId()){
			default:
				return true;
		}
	}

	/** Called when the add button is pressed */
	public void addElement(View view){
		EditText editText = (EditText) findViewById(R.id.edit_message);
		String element = editText.getText().toString();
		int i = 0;

		if(!lista.isEmpty()){
			for(String e :lista){
				if(element.compareToIgnoreCase(e)==0) return;
				else if(element.compareToIgnoreCase(e)<0) break;
				i++;
			}
		}

		lista.add(i,element);
		adapter.notifyDataSetChanged();
	}
}
