package hacs;

import java.util.*;

/**
 * Title: HACS Description: CSE870 Homework 3: Implementing Design Patterns
 * Copyright: Copyright (c) 2002 Company: Department of Computer Science and
 * Engineering, Michigan State University
 * 
 * @author Ji Zhang, Wei Zhu
 * @version 1.0
 * @author Sairachana Paladugu
 * @version 2.0 :: Update Code to 2021 Standards
 */

abstract public class Person {
	UserType type = UserType.Student;  // type=0 : student, type=1 instructor
	String userName;
	ClassCourseList courseList;
	CourseMenu theCourseMenu;
	Course currentCourse;
	Assignment currentAssignment;

	public Person() {
		courseList = new ClassCourseList();
	}

	abstract public CourseMenu createCourseMenu(Course theCourse, CourseLevel theLevel);

	/**
	 * show add button
	 */
	public void showAddButton() {
		theCourseMenu.showAddButtons();
	}

	/**
	 * show view button
	 */
	public void showViewButtons() {
		theCourseMenu.showViewButtons();
	}

	/**
	 * show communication box
	 */
	public void showComboxes() {
		theCourseMenu.showComboxes();
	}

	/**
	 * show radio buttons
	 */
	public void showRadios() {
		theCourseMenu.showRadios();
	}

	/**
	 * controls coursemenu window
	 */
	public void show() {
		theCourseMenu.setVisible(true);
	}

	/**
	 *
	 * logout method
	 * @return if user logged out
	 */
	public boolean ifLogout() {
		return theCourseMenu.ifLogout();
	}

	/**
	 * show the assignment list
	 * @return boolean value
	 */
	// show the assignment list
	public boolean showMenu() {
		// create a iterator for the assignment list
//    Iterator theIter=new ListIterator(CurrentCourse.AssList );
		Iterator<Assignment> theIterator = currentCourse.assignmentList.iterator();
		theCourseMenu.theCourse = currentCourse;
		Assignment theAssignment;
		while (theIterator.hasNext()) {
			theAssignment = (Assignment) theIterator.next();
			theCourseMenu.assignmentCombox.addItem(theAssignment);
		}
		return false;
	}

	public ClassCourseList GetCourseList() {
		return courseList;
	}

	public void addCourse(Course theCourse) {
		courseList.add(theCourse);
	}
}