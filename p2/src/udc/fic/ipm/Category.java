package udc.fic.ipm;

import java.util.ArrayList;

public class Category{

	ArrayList<String> items;
	String title;
	public Category(String title){
		this.title = title;
		items = new ArrayList<String>();
	}

	public String getTitle(){
		return title;
	}

	public ArrayList<String> getItems(){
		return items;
	}

	public void setItems(ArrayList<String> items){
		this.items = items;
	}

	public void setTitle(String title){
		this.title = title;
	}

	public boolean addItem(String item){
		int i = 0;
		for(String e: items){
			if(e.compareToIgnoreCase(item)==0) return false;
			if(e.compareToIgnoreCase(item)>0) break;
			i++;
		}

		items.add(i,item);
		return true;
	}
}
