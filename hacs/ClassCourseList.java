package hacs;

import java.util.ArrayList;
import java.io.*;
import java.util.Scanner;

/**
 * Title: HACS Description: Copyright: Copyright (c) 2002 Company: msu
 * 
 * @author Zhang ji Zhu Wei
 * @version 1.0
 * @author mjfindler
 * @version 2.0 update to Java 8
 * @author Sairachana Paladugu
 * @version 3.0 :: Update Code to 2021 Standards
 */

public class ClassCourseList extends ArrayList<Course> {

	public ClassCourseList() {
	}

	/**
	 * initialize the list by reading from the file.
	 * @param theFileName
	 */
	//// initialize the list by reading from the file.
	void initializeFromFile(String theFileName) {
		Scanner scanner;
		try {
			String strCourseName = null;
			File file = new File(theFileName);
			scanner = new Scanner(file);
			while (scanner.hasNextLine()) {
				strCourseName = scanner.nextLine();
				Course theCourse;
				theCourse = new Course(strCourseName, CourseLevel.HighLevel);
				//      theCourse.CourseName= strCourseName;
				add(theCourse);
			}

		} catch (Exception ee) {
			System.out.println(ee);

		}
	}

	/**
	 * @param CourseName
	 * @return matching course object
	 */
	Course findCourseByCourseName(String CourseName) {
		int nCourseCount = size();
		for (int i = 0; i < nCourseCount; i++) {
			Course theCourse;
			theCourse = (Course) get(i);
			if (theCourse.courseName.equals(CourseName))
				return theCourse;
		}
		return null;
	}

}