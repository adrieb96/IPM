package udc.fic.ipm;

import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.view.View;
import android.widget.TextView;

public class Show_Item extends Fragment{

	String item;

	public Show_Item(String item){
		this.item = item;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState){

		View rootView = inflater.inflate(R.layout.show_item,container,false);

		TextView tv = (TextView) rootView.findViewById(R.id.show_item);

		if(item != null) tv.setText(item);

		return rootView;		
	}
}
