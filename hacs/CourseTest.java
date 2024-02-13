package hacs;


import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Title: HACS Description: SER515 Assignment: UnitTest/Re-use
 *
 * @author Sairachana Paladugu
 * @version 1.0 :: Unit Tests added
 */
public class CourseTest {

    Course course;

    @BeforeEach
    void start() {
        course = new Course("SER423", CourseLevel.LowLevel);
    }

    /**
     * test addAssignment method in Course Class
     */
    @Test
    void testAddAssignment() {
        Assignment assignment = new Assignment();
        course.addAssignment(assignment);
        assertTrue(course.assignmentList.contains(assignment));
    }

    /**
     * test toString method in Course Class
     */
    @Test
    void testToString() {
        assertEquals(course.toString(), "SER423");
    }


}
