package hacs;

import java.util.*;

/**
 * Title: HACS Description: Copyright: Copyright (c) 2002 Company: msu
 * 
 * @author Zhang ji Zhu Wei
 * @version 1.0
 * @author mjfindler
 * @version 2.0 use <e> notation
 * @author Sairachana Paladugu
 * @version 3.0 :: Update Code to 2021 Design Standards
 */

public class ListIterator implements Iterator<Object> {
	ArrayList<Object> theList;
	int currentNumber = -1;

	public ListIterator() {
	}

	public ListIterator(ArrayList<Object> list) {
		theList = list;
	}

	/**
	 * checks for another item existence
	 * @return boolean value accordingly if next item exists or not
	 */
	public boolean hasNext() {
		if (currentNumber >= theList.size() - 1)
			return false;
		else
			return true;
	}

	/**
	 * moves iterator to next item
	 * @return next time
	 */
	public Object next() {
		if (hasNext() == true) {
			currentNumber++;
			return theList.get(currentNumber);
		} else {
			return null;
		}
	}

	/**
	 * removes the iterator currently pointed to
	 */
	public void remove() {
		theList.remove(currentNumber);
	}
}