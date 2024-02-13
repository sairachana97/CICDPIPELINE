package hacs;

import java.util.Iterator;
import java.util.*;

/**
 * Title: HACS Description: Copyright: Copyright (c) 2002 Company: msu
 * 
 * @author Zhang ji Zhu Wei
 * @version 1.0
 * @author mjfindler
 * @version 2.0 :: update to Java 8
 * @author Sairachana Paladugu
 * @version 3.0 :: Update Code to 2021 Standards
 */

/**
 * this class will iterate the course list attatched to on student and in turn
 * iterate the assignments of a course. after Function Visit(CourseList) it will
 * point to the location before the fist class, hasNext will retrun weather
 * there is next item. the next() will return the next Item Assignment;
 */

public class ReminderVisitor extends NodeVisitor {

	Reminder mReminder;

	public ReminderVisitor() {
	}

	public ReminderVisitor(Reminder reminder) {
		mReminder = reminder;
	}

	/**
	 * visit all courses from facade
	 * @param facade
	 */
	public void visitFacade(Facade facade) {
		CourseIterator courseList = new CourseIterator(facade.theCourseList);
		while (courseList.hasNext()) {
			Course course = (Course) courseList.next();
			course.accept(this);
		}
	}

	/**
	 * visit all assignments from course
	 * @param course
	 */
	public void visitCourse(Course course) {
		Iterator<Assignment> assignmentList = course.assignmentList.listIterator();
		while (assignmentList.hasNext()) {
			Assignment assignment = (Assignment) assignmentList.next();
			assignment.accept(this);
		}
	}

	/**
	 * visit all the assignments and reminders
	 * @param assignment
	 */
	public void visitAssignment(Assignment assignment) {
		Date today = new Date();
		Calendar calendar = Calendar.getInstance();
		calendar.setTime(today);
		int ntoday = calendar.get(Calendar.DAY_OF_YEAR);
		calendar.setTime(assignment.dueDate);
		int nDueDate = calendar.get(Calendar.DAY_OF_YEAR);
		if (nDueDate <= (ntoday + 1) && nDueDate >= ntoday) /// upcoming
		{
			mReminder.listUpcoming.add("Today is " + today.toString() + " " + assignment.assignmentName + " Due Date is "
					+ assignment.getDueDateString());
		}
		if (nDueDate < ntoday) {
			mReminder.listOverdue.add(assignment.assignmentName + " Due Date is " + assignment.getDueDateString());
		}

	}

}