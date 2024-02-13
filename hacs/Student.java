package hacs;

/**
 * Title: HACS Description: CSE870 Homework 3: Implementing Design Patterns
 * Copyright: Copyright (c) 2002 Company: Department of Computer Science and
 * Engineering, Michigan State University
 * 
 * @author Ji Zhang, Wei Zhu
 * @version 1.0
 */

public class Student extends Person {

	public Student() {
		type = UserType.Student; // type=0: student
	}

	/**
	 * @param theCourse
	 * @param theLevel
	 * @return Coursemenu
	 */
	public CourseMenu createCourseMenu(Course theCourse, CourseLevel theLevel) {

		if (theLevel == CourseLevel.HighLevel) {  // 0: Highlevel defined in CourseSelectDlg.
			theCourseMenu = new HighLevelCourseMenu();
		} else {  // 1: LowLevel
			theCourseMenu = new LowLevelCourseMenu();
		}
		return theCourseMenu;
	}

	@Override
	public boolean showMenu() {
		super.showMenu();
		showViewButtons();
		showComboxes();
		showRadios();
		show();
		return ifLogout();
	}
}