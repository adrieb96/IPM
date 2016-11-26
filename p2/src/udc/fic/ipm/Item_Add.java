package udc.fic.ipm;

import android.app.Fragment;
import android.os.Bundle;
import android.content.Context;

import android.view.LayoutInflater;
//import android.view.inputmethod.InputMethodManager;
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

	//private State state = State.ADD;
	//EditText editText;

	/*private InputMethodManager inputManager = (InputMethodManager) 
				((Main)getActivity()).getSystemService(Context.INPUT_METHOD_SERVICE);

	private enum State{
		ADD,
		EDIT };

*/
    /** Called when the activity is first created. */
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, 
			Bundle savedInstanceState){

		View rootView = inflater.inflate(R.layout.add_item,container,false);
		Button button = (Button) rootView.findViewById(R.id.add_button);

		button.setOnClickListener(new OnClickListener(){
			@Override
			public void onClick(View v){
				String text = getEditText();
				//if(state.equals(State.ADD))
					((Main)getActivity()).addItem(text);
				//else if(state.equals(State.EDIT))
				//	((Main)getActivity()).receiveItem(text);

				//inputManager.hideSoftInputFromWindow(editText.
					//getWindowToken(),0);

				//state = State.ADD;
			}
		});

		return rootView;
    }

	public String getEditText(){
		EditText editText = (EditText) getView().findViewById(R.id.text_edit);
		String element = editText.getText().toString().trim();

		editText.setText("");
		
		return element;
	}

	public void editItem(){
//		state = State.EDIT;
		//editText.setText(
		//inputManager.showSoftInput(editText, InputMethodManager.SHOW_IMPLICIT);
	}


}
