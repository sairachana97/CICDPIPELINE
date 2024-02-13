package hacs;


import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Title: HACS Description: SER515 Assignment: UnitTest/Re-use
 *
 * @author Sairachana Paladugu
 * @version 1.0 :: Unit Tests added
 */
public class InstructorTest {

    /**
     * this method test Createcoursemenu method for Lowlevel
     */
    @Test
    void testLowLevelCreateCourseMenu() {
        Course course = new Course("SER423", CourseLevel.LowLevel);
        Instructor instructor = new Instructor();
        assertTrue(instructor.createCourseMenu(course, CourseLevel.LowLevel) instanceof LowLevelCourseMenu);
    }

    /**
     * this method test create course menu for Highlevel
     */
    @Test
    void testHighLevelCreateCourseMenu() {
        Course course = new Course("SER423", CourseLevel.HighLevel);
        Instructor instructor = new Instructor();
        assertTrue(instructor.createCourseMenu(course, CourseLevel.HighLevel) instanceof HighLevelCourseMenu);
    }


}
