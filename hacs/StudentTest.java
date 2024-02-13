package hacs;

import org.junit.jupiter.api.Test;

import static org.junit.Assert.assertTrue;

/**
 * Title: HACS Description: SER515 Assignment: UnitTest/Re-use
 *
 * @author Sairachana Paladugu
 * @version 1.0 :: Unit Tests added
 */
public class StudentTest {

    /**
     *  tests createcourse menu for lowlevel
     */
    @Test
    void testLowLevelCreateCourseMenu() {
        Course course = new Course("SER515", CourseLevel.LowLevel);
        Student student = new Student();
        assertTrue(student.createCourseMenu(course, CourseLevel.LowLevel) instanceof LowLevelCourseMenu);
    }


    /**
     * tests createcoursemenu for highlevel
     */
    @Test
    void testHighLevelCreateCourseMenu() {
        Course course = new Course("SER515", CourseLevel.HighLevel);
        Student student = new Student();
        assertTrue(student.createCourseMenu(course, CourseLevel.HighLevel) instanceof HighLevelCourseMenu);
    }
}
