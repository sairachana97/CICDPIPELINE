package hacs;

/**
 * Title: HACS Description: Copyright: Copyright (c) 2002 Company: msu
 * 
 * @author Zhang ji Zhu Wei
 * @version 1.0
 *
 * @author Sairachana Paladugu
 * @version 2.0 :: Update Code to 2021 Standards
 */

public class Instructor extends Person {
	public Instructor() {
		type = UserType.Instructor; // type=1 :instructor
	}

	/**
	 *
	 * @param theCourse, theLevel
	 * @return thecoursemenu
	 */
	public CourseMenu createCourseMenu(Course theCourse, CourseLevel theLevel) {
		if (theLevel == CourseLevel.HighLevel) {  /// 0: Highlevel defined in CourseSeletDlg.
			theCourseMenu = new HighLevelCourseMenu();
		} else { /// 1: LowLevel
			theCourseMenu = new LowLevelCourseMenu();
		}
		return theCourseMenu;
	}

	public boolean showMenu() {
		super.showMenu();
		showAddButton();
		showViewButtons();
		showComboxes();
		showRadios();
		show();
		return ifLogout();
	}
}