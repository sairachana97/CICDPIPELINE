package hacs;

import java.util.Iterator;

/**
 * Title:        HACS
 * Description:
 * Copyright:    Copyright (c) 2002
 * Company:      msu
 * @author Zhang ji Zhu Wei
 * @version 1.0
 * @author Sairachana Paladugu
 * @version 2.0 :: Update Code to 2021 Standards
 */

public class SolutionIterator implements Iterator {
  SolutionList solutionList;

  int currentSolutionNumber = -1;
  ///  CurrentSolutionNumber: point to the location before the first element
  public SolutionIterator() {
  }
  public SolutionIterator(SolutionList thesolutionlist) {
    solutionList = thesolutionlist;
    MoveToHead();
  }

  /**
   * points to head element
   */
  public void MoveToHead() {
    ///  CurrentSolutionNumber: point to the location before the first element
    currentSolutionNumber=-1;
  }

  /**
   * @return boolean value if next item exists or not
   */
  public boolean hasNext() {
    /**@todo: Implement this java.util.Iterator method*/
    if (currentSolutionNumber >= solutionList.size() -1)
      return false;
    else
      return true;
    //    throw new java.lang.UnsupportedOperationException("Method hasNext() not yet implemented.");
  }
  public Solution next() {
    /**@todo: Implement this java.util.Iterator method*/
    if (hasNext()==true) {
      currentSolutionNumber ++;
      return solutionList.get(currentSolutionNumber);
    } else {
      return null;
    }
    //    throw new java.lang.UnsupportedOperationException("Method next() not yet implemented.");
  }

  /** get the next Solution that fits the Username;
   *
   * @param userName
   * @return
   */
  /// get the next Solution that fits the Username;
  public Solution next(String userName) {
    Solution theSolution;
    theSolution=(Solution)next();
    while(theSolution!=null) {
      if(userName.equals(theSolution.theAuthor)) {
        return theSolution;
      }
      theSolution = (Solution)next();
    }
    return null;
  }

  /**
   * remove current solution number
   */
  public void remove() {
    /**@todo: Implement this java.util.Iterator method*/
    currentSolutionNumber++;
    solutionList.remove(currentSolutionNumber);
    //    throw new java.lang.UnsupportedOperationException("Method remove() not yet implemented.");
  }


}