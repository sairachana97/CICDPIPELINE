package hacs;

import java.util.*;

/**
 * Title:        HACS
 * Description:  CSE870 Homework 3:  Implementing Design Patterns
 * Copyright:    Copyright (c) 2002
 * Company:      Department of Computer Science and Engineering, Michigan State University
 * @author Ji Zhang, Wei Zhu
 * @version 1.0
 * @author mjfindler
 * @version 2.0 
 * Update to Java 8
 * @author Sairachana Paladugu
 * @version 3.0 :: Update Code to 2021 Standards
 */

public class Course {
  String courseName;
  public ArrayList<Assignment> assignmentList = new ArrayList<Assignment>();
  int numberOfAssignments;
  CourseLevel courseLevel;


  public Course(String strCourse, CourseLevel theLevel) {
    this.courseName = strCourse;
    //0 HighLeve presentation    1  LowLevel Experiment
    this.courseLevel = theLevel;
    // this.AssList = NULL;
    this.numberOfAssignments = 0;
  }

  /**
   * This method adds an assignment to assignmentList
   *
   * @param newAssignment
   */
  public void addAssignment(Assignment newAssignment) {
    assignmentList.add(newAssignment);
    this.numberOfAssignments++;
  }

  /**
   * return course name as string
   *
   * @return coursename
   */
  public String toString() {
    return courseName;
  }
  
  void accept(NodeVisitor visitor) {
    visitor.visitCourse(this);
  }

}