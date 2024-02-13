package hacs;

/**
 * Title:        HACS
 * Description:  CSE870 Homework 3:  Implementing Design Patterns
 * Copyright:    Copyright (c) 2002
 * Company:      Department of Computer Science and Engineering, Michigan State University
 * @author Ji Zhang, Wei Zhu
 * @version 1.0
 * @author Sairachana Paladugu
 * @version 2.0 :: Update Code to 2021 Standards
 */

import java.util.*;
import java.text.DateFormat;

public class Assignment {

  protected String assignmentName;
  protected String strAssignmentFilename;
  protected Date dueDate = new Date();
  protected String assignmentSpecification;
  protected SolutionList theSolutionList = new SolutionList();
  protected Solution suggestedSolution = new Solution();



  public Assignment() {
  }

  /**
   *
   * set the due date
   *
   * @param theDueDate
   */
  public void setDueDate(Date theDueDate){

    this.dueDate = theDueDate;
  }

  /**
   *
   * set assignment specification
   *
   * @param theSpecification
   */
  public void setAssignmentSpecification(String theSpecification){

    this.assignmentSpecification = theSpecification;
  }

  /**
   * checks if assignment is overdue or not
   *
   * @return a boolean value according to the condition
   */
  public boolean isOverDue() {
    Date today;
    today = new Date();
    if (today.after(this.dueDate)) {
      return true;
    }
    else {
      return false;
    }
  }

  public Solution addSolution() {
    Solution mySolution = new Solution();
    return mySolution;
  }

  /**
   * add the theSolution to the Solutionlist
   *
   * @param theSolution
   */
  ////add the theSolution to the Solutionlist
  public void addSolution(Solution theSolution) {
    theSolutionList.add(theSolution);
  }

  /**
   * submit the solution to solution list
   *
   */
  public void submitSolution() {
  }

  /**
   * get the solution to solution list
   *
   */

  public void getSolutionList() {
  }

  /**
   * return the solution of the give name
   *
   * @param studentName
   * @return
   */
  /* return the solution of the give name
   */
  public Solution getSolution(String studentName) {
    SolutionIterator iterator = new SolutionIterator(theSolutionList);
    return (Solution) iterator.next(studentName);
  }

  /**
   * get the suggested solution
   *
   * @return the suggested solution
   */
  public Solution getSuggestedSolution() {
    return suggestedSolution;
  }

  /**
   * get the solution iterator
   *
   * @return solution iterator
   */
  public SolutionIterator getSolutionIterator() {
    SolutionIterator theSolutionIterator = new SolutionIterator(theSolutionList);
    return theSolutionIterator;
  }

  /**
   * get the assignment name as string
   *
   * @return assignment name as string
   */
  public String toString() {

    return assignmentName;
  }

  /**
   * get due date as string
   *
   * @return due date as string
   */
  public String getDueDateString() {
    DateFormat dateFormat = DateFormat.getDateInstance(DateFormat.SHORT);
    return  dateFormat.format(dueDate);
  }

  public void accept(NodeVisitor visitor) {
    visitor.visitAssignment(this);
  }
}