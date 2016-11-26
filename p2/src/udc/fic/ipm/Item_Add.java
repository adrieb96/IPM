package udc.fic.ipm;

import android.app.Fragment;
import android.os.Bundle;

import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.view.View;
import android.view.View.OnClickListener;

import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.List;

public class Item_Add extends Fragment{

	View rootView = null;

    /** Called when the activity is first created. */
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, 
			Bundle savedInstanceState){

		rootView = inflater.inflate(R.layout.add_item,container,false);
		Button button = (Button) rootView.findViewById(R.id.add_button);

		button.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v){
				String text = getEditText();
				((Main)getActivity()).addItem(text);
				//((Main)getActivity()).throwToast(text);				
			}
		});

		return rootView;
    }

	public String getEditText(){
		EditText editText = (EditText) rootView.findViewById(R.id.text_edit);
		String element = editText.getText().toString().trim();

		editText.setText("");
		
		return element;
	}

}
